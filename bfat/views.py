from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from allianceauth.authentication.decorators import permissions_required
import allianceauth.eveonline
import os
from django.conf import settings
from esi.decorators import token_required
from .models import Fat, FatLink, ManualFat
from allianceauth.eveonline.models import EveAllianceInfo
from allianceauth.eveonline.models import EveCharacter
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.eveonline.providers import provider
from .forms import FatLinkForm
from django.utils.crypto import get_random_string


if hasattr(settings, 'FAT_AS_PAP'):
    term = 'PAP'
else:
    term = 'FAT'

SWAGGER_SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')
"""
Swagger Operations:

get_characters_character_id_fleet
get_fleets_fleet_id
get_fleets_fleet_id_members
get_characters_character_id
get_universe_systems_system_id
get_universe_types_type_id
get_search
"""


# Create your views here.
@login_required()
def bfat_view(request):
    ctx = {'term': term}
    return render(request, 'bfat/bfatview.html', ctx)


@login_required()
def stats(request):
    pass


@login_required()
def links(request):
    pass


@login_required()
@permissions_required(('bfat.manage_bfat', 'bfat.addfatlink'))
@token_required(
    scopes=['esi-fleets.read_fleet.v1'])
def link_add(request, token):
    # "error": "The fleet does not exist or you don't have access to it!"
    hash = get_random_string(length=30)
    link = FatLink(fleet=" ", creator=request.user, hash=hash)
    link.save()

    # Check if there is a fleet
    c = token.get_esi_client(spec_file=SWAGGER_SPEC_PATH)
    f = c.Fleets.get_characters_character_id_fleet(character_id=token.character_id).result()
    if 'error' not in f:
        fleet = c.Fleets.get_fleets_fleet_id(fleet_id=f['fleet_id']).result()
        if 'error' not in fleet:
            m = c.Fleets.get_fleets_fleet_id_members(fleet_id=f['fleet_id']).result()
            ch = []
            for char in m:
                char_id = char['character_id']
                sol_id = char['solar_system_id']
                ship_id = char['ship_type_id']

                solar_system = c.Universe.get_universe_systems_system_id(system_id=sol_id).result()
                ship = c.Universe.get_universe_types_type_id(type_id=ship_id).result()

                sol_name = solar_system['name']
                ship_name = ship['name']

                character, created = EveCharacter.objects.get_or_create(character_id=char_id)
                ch.append((character, created))
                link = FatLink.objects.get(hash=hash)
                fat = Fat(fatlink_id=link.pk, character=character, system=sol_name, shiptype=ship_name).save()

            ctx = {'form': FatLinkForm, 'term': term, 'hash': hash, 'debug': ch}

    return render(request, 'bfat/fleet_add.html', ctx)


@login_required()
def edit_link(request):
    pass


@login_required()
def del_link(request):
    pass
