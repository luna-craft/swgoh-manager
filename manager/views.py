from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Guild, Player, Character, Unit

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