from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import allianceauth.eveonline
import os

SWAGGER_SPEC_PATH = os.path.join(allianceauth.eveonline.__path__, 'swagger.json')
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
    return render(request, 'bfatview.html')