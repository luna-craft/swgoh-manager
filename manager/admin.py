from django.contrib import admin
from .models import Guild, Player, Character, Unit, Squad

class UnitAdmin(admin.ModelAdmin):
    list_display = ('character', 'player', 'rarity', 'level', 'gear_level', 'power')
    search_fields = ['character__name', 'player__player_name']


class SquadAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ('id', 'name', 'category', 'char1', 'char2', 'char3', 'char4', 'char5',)
    search_fields = ['char1__name', 'char2__name', 'char3__name', 'char4__name', 'char5__name', ]

admin.site.register(Guild)
admin.site.register(Player)
admin.site.register(Character)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Squad, SquadAdmin)

