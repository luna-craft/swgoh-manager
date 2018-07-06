from django.contrib import admin
from .models import Guild, Player, Character, Unit, Squad

class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'guild_id', 'active')
    search_fields = ['name']


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'guild', 'active')
    search_fields = ['name']


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'combat_type', 'power')
    list_filter = ['combat_type']
    search_fields = ['name']


class UnitAdmin(admin.ModelAdmin):
    list_filter = ['rarity', 'gear_level']
    list_display = ('character', 'player', 'rarity', 'level', 'gear_level', 'power')
    search_fields = ['character__name', 'player__player_name']


class SquadAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ('name', 'category', 'char1', 'char2', 'char3', 'char4', 'char5',)
    search_fields = ['char1__name', 'char2__name', 'char3__name', 'char4__name', 'char5__name', ]


admin.site.register(Guild, GuildAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Squad, SquadAdmin)

