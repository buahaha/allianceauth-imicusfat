from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from allianceauth.authentication.decorators import permissions_required
import os
from django.core.paginator import Paginator
from django.conf import settings
from esi.decorators import token_required
from .models import Fat, FatLink, ManualFat, DelLog
from allianceauth.eveonline.models import EveAllianceInfo, EveCharacter, EveCorporationInfo
from allianceauth.authentication.models import CharacterOwnership
from .forms import FatLinkForm, ManualFatForm, FlatListForm
from django.utils.crypto import get_random_string
from .tasks import get_or_create_char, process_fats


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
    msg = None
    if 'msg' in request.session:
        msg = request.session.pop('msg')
    chars = CharacterOwnership.objects.filter(user=request.user)
    fats = []
    for char in chars:
        fat = Fat.objects.filter(character=char.character).order_by('fatlink__fattime').reverse()[:30]
        char_1 = [char.character.character_name]
        for f in fat:
            char_1.append(f)
        fats.append(char_1)
    links = FatLink.objects.order_by('fattime').reverse()[:10]
    ctx = {'term': term, 'fats': fats, 'links': links, 'msg': msg}
    return render(request, 'bfat/bfatview.html', ctx)


@login_required()
def stats(request):
    pass


@login_required()
def links(request, page=1):
    links = FatLink.objects.all().order_by('fattime').reverse()
    pages = Paginator(links, 15)
    links = pages.page(page)
    ctx = {'term': term, 'links': links}
    return render(request, 'bfat/fat_list.html', ctx)


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
            process_fats.delay(m, 'eve', hash)

            request.session['{}-creation-code'.format(hash)] = 200
            return redirect('bfat:link_edit', hash=hash)
        except:
            request.session['{}-creation-code'.format(hash)] = 403
            return redirect('bfat:link_edit', hash=hash)
    except:
        request.session['{}-creation-code'.format(hash)] = 404
        return redirect('bfat:link_edit', hash=hash)


@login_required()
@permissions_required(('bfat.manage_bfat', 'bfat.add_fatlink', 'bfat.edit_fatlink'))
def edit_link(request, hash=None):
    if hash is None:
        request.session['msg'] = ['warning', 'No {}link hash provided.'.format(term)]
        return redirect('bfat:bfat_view')
    try:
        link = FatLink.objects.get(hash=hash)
    except:
        request.session['msg'] =['warning', 'The hash provided is not valid.']
        return redirect('bfat:bfat_view')
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
            flatlist = request.POST['flatlist']
            formatted = flatlist.replace("\r", "").split("\n")
            process_fats.delay(formatted, 'flatlist', hash)
            request.session['{}-task-code'.format(hash)] = 2
        elif f3.is_valid():
            form = request.POST
            character_name = form['character']
            system = form['system']
            shiptype = form['shiptype']
            creator = request.user
            character = get_or_create_char(name=character_name)
            if character is not None:
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
    flatlist = None
    if len(fats) > 0:
        flatlist = []
        for fat in fats:
            fatinfo = [fat.character.character_name, str(fat.system), str(fat.shiptype)]
            flatlist.append("\t".join(fatinfo))
        flatlist = "\r\n".join(flatlist)

    ctx = {'term': term, 'form': FatLinkForm, 'msg': msg, 'link': link, 'fats': fats, 'flatlist': flatlist,
           'debug': debug}
    return render(request, 'bfat/fleet_edit.html', ctx)


@login_required()
@permissions_required(('bfat.manage_bfat', 'bfat.delete_fatlink'))
def del_link(request, hash=None):
    if hash is None:
        request.session['msg'] = ['warning', 'No {}link hash provided.'.format(term)]
        return redirect('bfat:bfat_view')
    try:
        link = FatLink.objects.get(hash=hash)
    except:
        request.session['msg'] = ['danger', 'The hash provided is either invalid or has been deleted.']
        return redirect('bfat:bfat_view')
    link.delete()
    DelLog(remover=request.user, deltype=0, string=link.__str__()).save()
    request.session['msg'] = ['success', 'The {0}Link ({1}) and all associated {0}s have been successfully deleted.'.format(term, hash)]
    return redirect('bfat:bfat_view')


@login_required()
@permissions_required(('bfat.manage_bfat', 'bfat.delete_fat', 'bfat.delete_fatlink'))
def del_fat(request, hash, fat):
    try:
        link = FatLink.objects.get(hash=hash)
    except:
        request.session['msg'] = ['danger', 'The hash provided is either invalid or has been deleted.']
        return redirect('bfat:bfat_view')
    try:
        fat = Fat.objects.get(pk=fat, fatlink_id=link.pk)
    except:
        request.session['msg'] = ['danger', 'The hash and {} ID do not match.'.format(term)]
        return redirect('bfat:bfat_view')
    fat.delete()
    DelLog(remover=request.user, deltype=1, string=fat.__str__())
    request.session['msg'] = ['success', 'The {0} for {0} from link {1} has been successfully deleted.'.format(term, hash)]
    return redirect('bfat:bfat_view')
