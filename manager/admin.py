from django.contrib import admin
from django.utils.html import format_html
from .models import Guild, Player, Character, Unit, Squad, RequiredUnit, PlayerStat

class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'guild_id', 'active')
    search_fields = ['name']


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'guild', 'ally_code', 'show_swgoh_url', 'active')
    list_filter = ['guild']
    search_fields = ['name']

    def show_swgoh_url(self, obj):
        return format_html("<a href='https://swgoh.gg/u/{url}' target='_blank' referrerpolicy='no-referrer'>{url}</a>", url=obj.swgoh_name)
    show_swgoh_url.short_description = "SWGOH.GG Page"

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'combat_type', 'power')
    list_filter = ['combat_type']
    search_fields = ['name']


class UnitAdmin(admin.ModelAdmin):
    list_filter = ['rarity', 'gear_level', 'character']
    list_display = ('character', 'player', 'rarity', 'level', 'gear_level', 'power')
    search_fields = ['character__name', 'player__player_name']


class SquadAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ('name', 'category', 'char1', 'char2', 'char3', 'char4', 'char5',)
    search_fields = ['char1__name', 'char2__name', 'char3__name', 'char4__name', 'char5__name', ]


class RequiredUnitAdmin(admin.ModelAdmin):
    list_display = ('character', 'player', 'rarity', 'gear_level')
    search_fields = ['character__name', 'player__player_name']


class PlayerStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'week', 'total_energy', 'total_power', 'total_chars')
    search_fields = ['player__player_name']

admin.site.register(Guild, GuildAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Squad, SquadAdmin)
admin.site.register(RequiredUnit, RequiredUnitAdmin)
admin.site.register(PlayerStat, PlayerStatAdmin)

