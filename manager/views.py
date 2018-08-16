from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Guild, Player, Character, Unit, Squad, RequiredUnit

def index(request):
    try:
        guild = Guild.objects.filter(active=True)[0]
    except Guild.DoesNotExist:
        raise Http404("Guild does not exist")
    return render(request, 'manager/index.html', {'guild': guild})


def character(request, character_id):
    try:
        character = Character.objects.get(pk=character_id)
    except Character.DoesNotExist:
        raise Http404("Character does not exist")
    return render(request, 'manager/character.html', {'character': character})


def players(request):
    guild = Guild.objects.filter(active=True)[0]
    players = Player.objects.filter(guild=guild).order_by('-total_power')
    # Отсортировать по количеству готовых отрядов
    sorted_data = sorted(players, key=lambda k: k.total_power, reverse=True)
    return render(request, 'manager/players.html', {'players': players, 'guild': guild,})


def player(request, player_id):
    try:
        # игрок
        player = Player.objects.get(pk=player_id)
        # список заданий на прокачку
        required_units = {player: [ru for ru in RequiredUnit.objects.filter(player=player)]}
        # сформировать список всех отрядов и их готовность
        squads = Squad.objects.all()
        data = []
        for squad in squads:
            squad_data = squad.populate_units(player=player, required_units=required_units,
                can_require=request.user.is_authenticated).get(player.id)
            data.append(squad_data)
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render(request, 'manager/player.html', {'player': player, 'squads': data, 'required_units': required_units[player]})


def squads(request):
    guild = Guild.objects.filter(active=True)[0]
    squads = Squad.objects.all()
    return render(request, 'manager/squads.html', {'squads': squads, 'guild': guild,})


def _make_squad_query(squad):
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
    return query

def squad_json(request, squad_id):
    try:
        squad = Squad.objects.get(pk=squad_id)
        jsondata = {'name': squad.name, 'category': squad.category,
                'char1': squad.char1.base_id if squad.char1 else '',
                'char2': squad.char2.base_id if squad.char2 else '',
                'char3': squad.char3.base_id if squad.char3 else '',
                'char4': squad.char4.base_id if squad.char4 else '',
                'char5': squad.char5.base_id if squad.char5 else '',
                'units': []}
        units = Unit.objects.filter(_make_squad_query(squad)).order_by('player__player_name')
        for unit in units:
            jsondata['units'].append({'base_id': unit.character.base_id, 'player': unit.player.player_name, 'rarity': unit.rarity, 'level': unit.level, 'gear': unit.gear_level, 'power': unit.power})
    except Squad.DoesNotExist:
        raise Http404("Squad does not exist")
    return JsonResponse(jsondata)



def squad(request, squad_id):
    try:
        guild = Guild.objects.filter(active=True)[0]
        squad = Squad.objects.get(pk=squad_id)
        # список заданий на прокачку
        required_units = {}
        for ru in RequiredUnit.objects.filter(_make_squad_query(squad)):
            if not required_units.get(ru.player):
                required_units[ru.player] = [ru]
            else:
                required_units[ru.player].append(ru)
        # данные по отряду
        data = squad.populate_units(guild=guild, required_units=required_units, can_require=request.user.is_authenticated)
        # Отсортировать по мощи пачки
        sorted_data = sorted(data.values(), key=lambda k: k['power'], reverse=True)
        can_require = request.user.is_authenticated
    except Guild.DoesNotExist:
        raise Http404("No active guild")
    except Squad.DoesNotExist:
        raise Http404("Squad does not exist")
    return render(request, 'manager/squad.html', {'guild': guild, 'squad': squad, 'units': sorted_data,
        'required_units': [ru for values in required_units.values() for ru in values]})


def require_unit(request, player_id, character_id):
    try:
        player = Player.objects.get(pk=player_id)
        units = Unit.objects.filter(player=player)
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    except Character.DoesNotExist:
        raise Http404("Character does not exist")
    return render(request, 'manager/character.html', {'character': character})


def rancor(request):
    try:
        solo = Character.objects.get(base_id='HANSOLO')
        guild = Guild.objects.filter(active=True)[0]
        players = Player.objects.filter(guild=guild)
        units = Unit.objects.filter(character=solo, player__in=players)
        rancor = []
        norancor = []
        for player in players:
            matches = [u for u in units if u.player == player]
            if matches:
                unit = matches[0]
                if unit.rarity == 7:
                    norancor.append({'player': player, 'rarity': unit.rarity, 'level': unit.level, 'gear_level': unit.gear_level, 'power': unit.power})
                else:
                    rancor.append({'player': player, 'rarity': unit.rarity, 'level': unit.level, 'gear_level': unit.gear_level, 'power': unit.power})
            else:
                rancor.append({'player': player, 'rarity': 0, 'level': 0, 'gear_level': 0, 'power': 0})
    except Character.DoesNotExist:
        raise Http404("Han Solor character not found")
    except Guild.DoesNotExist:
        raise Http404("Guild does not exist")
    return render(request, 'manager/rancor.html', {'guild': guild, 'players': players, 'units': units, 'rancor': rancor, 'norancor': norancor})