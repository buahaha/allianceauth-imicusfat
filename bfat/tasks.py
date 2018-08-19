from esi.clients import esi_client_factory
from allianceauth.eveonline.models import EveAllianceInfo, EveCharacter, EveCorporationInfo
from .views import SWAGGER_SPEC_PATH


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