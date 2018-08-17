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


if hasattr(settings, 'FAT_AS_PAP'):
    term = 'PAP'
else:
    term = 'FAT'

SWAGGER_SPEC_PATH = os.path.join(allianceauth.eveonline.__path__[0], 'swagger.json')
"""
Swagger Operations:

get_characters_character_id_fleet
get_fleets_fleet_id
get_fleets_fleet_id_members
get_characters_character_id
get_universe_systems_system_id
get_universe_stations_station_id
get_universe_structures_structure_id
get_universe_types_type_id
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
def add_link(request, token):
    if request.method == "POST":
        ctx = {'form': FatLinkForm, 'term': term}
    elif request.method == "PUT":
        pass
    else:
        pass
    return render(request, 'bfat/add_link.html', ctx)


@login_required()
def edit_link(request):
    pass


@login_required()
def del_link(request):
    pass
