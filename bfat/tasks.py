from esi.clients import esi_client_factory
from allianceauth.eveonline.models import EveAllianceInfo, EveCharacter, EveCorporationInfo
import os
from .models import Fat, FatLink
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

SWAGGER_SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

class NoDataError(Exception):
    def __init__(self, msg):
        Exception.__init__(self,msg)


def get_or_create_char(name: str=None, id: int=None):
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
        c = esi_client_factory(spec_file=SWAGGER_SPEC_PATH)
        result = c.Search.get_search(categories=['character'], search=name, strict=True).result()
        if 'character' not in result:
            return None
        char_id = result['character'][0]
        qs = EveCharacter.objects.filter(character_id=char_id)
    elif id:
        # If an ID is passed we can just check the db for it.
        qs = EveCharacter.objects.filter(character_id=char_id)
    elif not name and not id:
        raise NoDataError("No character name or id provided.")

    if len(qs) == 0:
        # Create Character
        character = EveCharacter.objects.create_character(char_id)
        character = EveCharacter.objects.get(pk=character.pk)
        # Make corp and alliance info objects for future sane
        if character.alliance_id is not None:
            test = EveAllianceInfo.objects.filter(alliance_id=character.alliance_id)
            if len(test) == 0:
                EveAllianceInfo.objects.create_alliance(character.alliance_id)
        else:
            test = EveCorporationInfo.objects.filter(corporation_id=character.corporation_id)
            if len(test) == 0:
                EveCorporationInfo.objects.create_corporation(character.corporation_id)

    else:
        character = qs[0]

    return character

@shared_task
def process_fats(list, type_, hash):
    """
    Due to the large possible size of fatlists, this process will be scheduled in order to process flat_lists.
    :param list: the list of character info to be processed.
    :param type: flatlist or eve
    :param hash: the hash from the fat link.
    :return:
    """
    link = FatLink.objects.get(hash=hash)
    c = esi_client_factory(spec_file=SWAGGER_SPEC_PATH)
    if type_ == 'flatlist':
        if len(list[0]) > 40:
            # Came from fleet comp
            for line in list:
                data = line.split("\t")
                process_line.delay(data, 'comp', link)
        else:
            # Came from chat window
            for char in list:
                process_line.delay(char, 'chat', link)
    elif type_ == 'eve':
        for char in list:
            process_character.delay(char, link)

@shared_task
def process_line(line, type_, link):
    if type_ == 'comp':
        character = get_or_create_char(name=line[0].strip(" "))
        system = line[1].strip(" (Docked)")
        shiptype = line[2]
        if character is not None:
            fat = Fat(fatlink_id=link.pk, character=character, system=system, shiptype=shiptype).save()
    else:
        character = get_or_create_char(name=line.strip(" "))
        if character is not None:
            fat = Fat(fatlink_id=link.pk, character=character).save()


@shared_task
def process_character(char, link):
    c = esi_client_factory(spec_file=SWAGGER_SPEC_PATH)
    char_id = char['character_id']
    sol_id = char['solar_system_id']
    ship_id = char['ship_type_id']

    solar_system = c.Universe.get_universe_systems_system_id(system_id=sol_id).result()
    ship = c.Universe.get_universe_types_type_id(type_id=ship_id).result()

    sol_name = solar_system['name']
    ship_name = ship['name']
    character = get_or_create_char(id=char_id)
    link = FatLink.objects.get(hash=hash)
    fat = Fat(fatlink_id=link.pk, character=character, system=sol_name, shiptype=ship_name).save()