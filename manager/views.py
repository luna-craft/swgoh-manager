from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Guild, Player, Character, Unit, Squad

def index(request):
    players = Player.objects.all()
    context = {'players': players,}
    return render(request, 'manager/index.html', context)


def player(request, player_id):
    try:
        player = Player.objects.get(pk=player_id)
        units = Unit.objects.filter(player=player)
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render(request, 'manager/player.html', {'player': player, 'units': units})


def squads(request):
    squads = Squad.objects.all()
    return render(request, 'manager/squads.html', {'squads': squads})


def squad(request, squad_id):
    try:
        squad = Squad.objects.get(pk=squad_id)
        jsondata = {'name': squad.name, 'category': squad.category, 
                'char1': squad.char1.base_id if squad.char1 else '',
                'char2': squad.char2.base_id if squad.char2 else '',
                'char3': squad.char3.base_id if squad.char3 else '',
                'char4': squad.char4.base_id if squad.char4 else '',
                'char5': squad.char5.base_id if squad.char5 else '',
                'units': []}
        query = Q()
        if squad.char1:
            query = query | Q(character=squad.char1)
        if squad.char2:
            query = query | Q(character=squad.char2)
        if squad.char3:
            query = query | Q(character=squad.char3)
        if squad.char4:
            query = query | Q(character=squad.char4)
        if squad.char5:
            query = query | Q(character=squad.char5)            
        units = Unit.objects.filter(query).order_by('player__player_name')
        for unit in units:
            jsondata['units'].append({'base_id': unit.character.base_id, 'player': unit.player.player_name, 'rarity': unit.rarity, 'level': unit.level, 'gear': unit.gear_level, 'power': unit.power})
    except Squad.DoesNotExist:
        raise Http404("Squad does not exist")
    return JsonResponse(jsondata)
