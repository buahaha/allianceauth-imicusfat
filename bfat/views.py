from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from allianceauth.authentication.decorators import permissions_required
import allianceauth.eveonline
import os
from django.conf import settings
from esi.decorators import token_required
from esi.clients import esi_client_factory
from .models import Fat, FatLink, ManualFat
from allianceauth.eveonline.models import EveAllianceInfo
from allianceauth.eveonline.models import EveCharacter
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.eveonline.providers import provider
from allianceauth.authentication.models import CharacterOwnership
from .forms import FatLinkForm, ManualFatForm, FlatListForm
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
get_corporation_corporation_id
get_alliance_alliance_id
"""

# Create your views here.
@login_required()
def bfat_view(request):
    chars = CharacterOwnership.objects.filter(user=request.user)
    fats = []
    for char in chars:
        fat = Fat.objects.filter(character=char.character).order_by('fatlink__fattime').reverse()[:30]
        char_1 = [char.character.character_name]
        for f in fat:
            char_1.append(f)
        fats.append(char_1)
    links = FatLink.objects.order_by('fattime').reverse()[:10]
    ctx = {'term': term, 'fats': fats, 'links': links}
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
    link = FatLink(fleet=None, creator=request.user, hash=hash)
    link.save()

    # Check if there is a fleet
    c = token.get_esi_client(spec_file=SWAGGER_SPEC_PATH)
    try:
        f = c.Fleets.get_characters_character_id_fleet(character_id=token.character_id).result()
        try:
            fleet = c.Fleets.get_fleets_fleet_id(fleet_id=f['fleet_id']).result()
            m = c.Fleets.get_fleets_fleet_id_members(fleet_id=f['fleet_id']).result()
            for char in m:
                char_id = char['character_id']
                sol_id = char['solar_system_id']
                ship_id = char['ship_type_id']

                solar_system = c.Universe.get_universe_systems_system_id(system_id=sol_id).result()
                ship = c.Universe.get_universe_types_type_id(type_id=ship_id).result()

                sol_name = solar_system['name']
                ship_name = ship['name']

                character = EveCharacter.objects.filter(character_id=char_id)
                if len(character) == 0:
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
                    character = character[0]
                link = FatLink.objects.get(hash=hash)
                fat = Fat(fatlink_id=link.pk, character=character, system=sol_name, shiptype=ship_name).save()

            request.session['{}-creation-code'.format(hash)] = 200
            return redirect('bfat:link_edit', hash=hash)
        except:
            request.session['{}-creation-code'.format(hash)] = 403
            return redirect('bfat:link_edit', hash=hash)
    except:
        request.session['{}-creation-code'.format(hash)] = 404
        return redirect('bfat:link_edit', hash=hash)


@login_required()
def edit_link(request, hash=None):
    link = FatLink.objects.get(hash=hash)
    debug = None
    if request.method == "POST":
        f1 = FatLinkForm(request.POST)
        f2 = FlatListForm(request.POST)
        f3 = ManualFatForm(request.POST)
        if f1.is_valid():
            link.fleet = request.POST['fleet']
            link.save()
            request.session['{}-task-code'.format(hash)] = 1
        elif f2.is_valid():
            # Process flat list here.
            debug = request.POST
            pass
        elif f3.is_valid():
            form = request.POST
            character_name = form['character']
            system = form['system']
            shiptype = form['shiptype']
            creator = request.user
            c = esi_client_factory(spec_file=SWAGGER_SPEC_PATH)
            results = c.Search.get_search(categories=['character'], search=character_name, strict=True).result()
            character_id = results['character'][0]
            if 'character' in results:
                character = EveCharacter.objects.filter(character_id=character_id)
                if len(character) == 0:
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
                    character = character[0]

                fat = Fat(fatlink_id=link.pk, character=character, system=system, shiptype=shiptype).save()
                ManualFat(fatlink_id=link.pk, creator=creator, character=character).save()
                request.session['{}-task-code'.format(hash)] = 3
            else:
                request.session['{}-task-code'.format(hash)] = 4
        else:
            request.session['{}-task-code'.format(hash)] = 0
    msg = None
    if '{}-creation-code'.format(hash) in request.session:
        msg = request.session.pop('{}-creation-code'.format(hash))
    elif '{}-task-code'.format(hash) in request.session:
        msg = request.session.pop('{}-task-code'.format(hash))
    fats = Fat.objects.filter(fatlink=link)
    ctx = {'term': term, 'form': FatLinkForm, 'msg': msg, 'link': link, 'fats': fats, 'debug': debug}
    return render(request, 'bfat/fleet_edit.html', ctx)


@login_required()
def del_link(request):
    pass
