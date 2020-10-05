# -*- coding: utf-8 -*-

"""
tasks
"""

from celery import shared_task

from imicusfat import __title__
from imicusfat.models import IFat, IFatLink
from imicusfat.providers import esi
from imicusfat.utils import LoggerAddTag

from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger


logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class NoDataError(Exception):
    """
    NoDataError
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


def get_or_create_char(name: str = None, id: int = None):
    """
    This function takes a name or id of a character and checks to see if the character already exists.
    If the character does not already exist, it will create the character object, and if needed the corp/alliance
    objects as well.
    :param name: str (optional)
    :param id: int (optional)
    :returns character: EveCharacter
    """

    if name:
        # If a name is passed we have to check it on ESI
        result = esi.client.Search.get_search(
            categories=["character"], search=name, strict=True
        ).result()

        if "character" not in result:
            return None

        id = result["character"][0]
        eve_character = EveCharacter.objects.filter(character_id=id)
    elif id:
        # If an ID is passed we can just check the db for it.
        eve_character = EveCharacter.objects.filter(character_id=id)
    elif not name and not id:
        raise NoDataError("No character name or id provided.")

    if len(eve_character) == 0:
        # Create Character
        character = EveCharacter.objects.create_character(id)
        character = EveCharacter.objects.get(pk=character.pk)

        # Make corp and alliance info objects for future sane
        if character.alliance_id is not None:
            test = EveAllianceInfo.objects.filter(alliance_id=character.alliance_id)

            if len(test) == 0:
                EveAllianceInfo.objects.create_alliance(character.alliance_id)
        else:
            test = EveCorporationInfo.objects.filter(
                corporation_id=character.corporation_id
            )

            if len(test) == 0:
                EveCorporationInfo.objects.create_corporation(character.corporation_id)

    else:
        character = eve_character[0]

    logger.info("Processing information for character %s", character.pk)

    return character


@shared_task
def process_fats(list, type_, hash):
    """
    Due to the large possible size of fatlists, this process will be scheduled in order to process flat_lists.
    :param list: the list of character info to be processed.
    :param type_: only "eve" for now
    :param hash: the hash from the fat link.
    :return:
    """
    logger.info("Processing FAT %s", hash)

    if type_ == "eve":
        for char in list:
            process_character.delay(char, hash)


@shared_task
def process_line(line, type_, hash):
    """
    process_line
    processing every single character on its own
    :param line:
    :param type_:
    :param hash:
    :return:
    """

    link = IFatLink.objects.get(hash=hash)

    if type_ == "comp":
        character = get_or_create_char(name=line[0].strip(" "))
        system = line[1].strip(" (Docked)")
        shiptype = line[2]

        if character is not None:
            IFat(
                ifatlink_id=link.pk,
                character=character,
                system=system,
                shiptype=shiptype,
            ).save()
    else:
        character = get_or_create_char(name=line.strip(" "))

        if character is not None:
            IFat(ifatlink_id=link.pk, character=character).save()


@shared_task
def process_character(char, hash):
    """
    process_character
    :param char:
    :param hash:
    :return:
    """

    link = IFatLink.objects.get(hash=hash)

    char_id = char["character_id"]
    sol_id = char["solar_system_id"]
    ship_id = char["ship_type_id"]

    solar_system = esi.client.Universe.get_universe_systems_system_id(
        system_id=sol_id
    ).result()
    ship = esi.client.Universe.get_universe_types_type_id(type_id=ship_id).result()

    sol_name = solar_system["name"]
    ship_name = ship["name"]
    character = get_or_create_char(id=char_id)

    IFat(
        ifatlink_id=link.pk, character=character, system=sol_name, shiptype=ship_name
    ).save()

    logger.info("Processing information for character with ID %s", character)
