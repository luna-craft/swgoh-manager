#!/usr/bin/env python3
import requests
import json
from .models import *


def update_character_database():
    # загрузить базу данных персонажей
    response = requests.get('https://swgoh.gg/api/characters')
    json_data = response.json()
    for idx, c in enumerate(json_data):
        found = Character.objects.filter(base_id=c['base_id'])
        if len(found) == 0:
            character = Character(base_id=c['base_id'], name=c['name'], power=c['power'], description=c['description'], url=c['url'], image=c['image'], combat_type=c['combat_type'])
        else:
            character = found[0]
            character.name = c['name']
            character.power = c['power']
            character.description = c['description']
            character.url = c['url']
            character.image = c['image']
            character.combat_type = c['combat_type']
        character.save()
    # загрузить базу данных кораблей
    response = requests.get('https://swgoh.gg/api/ships')
    json_data = response.json()
    for c in json_data:
        found = Character.objects.filter(base_id=c['base_id'])
        if len(found) == 0:
            character = Character(base_id=c['base_id'], name=c['name'], power=c['power'], description=c['description'], url=c['url'], image=c['image'], combat_type=c['combat_type'])
        else:
            character = found[0]
            character.name = c['name']
            character.power = c['power']
            character.description = c['description']
            character.url = c['url']
            character.image = c['image']
            character.combat_type = c['combat_type']
        character.save()


#response = requests.get('https://swgoh.gg/api/guilds/34508/units')
#json_data = response.json()
#with open('units.json','w+') as file:
#    json.dump(json_data, file)

def update_guild(guild):
    # Запрос в свгох
    response = requests.get('https://swgoh.gg/api/guilds/%d/units' % guild.guild_id)
    root = lxml.html.fromstring(response.text)
    players = root.cssselect('.character-list table tbody tr td:first-child')
    # добавить или обновить игроков из ги
    for p in players:
        name = p.attrib['data-sort-value']
        login = p[0].attrib['href'][3:-1]
        found = Player.objects.filter(swgoh_name=login)
        if len(found) == 0:
                player = Player(player_name=name, swgoh_name=login, guild=guild, active=True)
        else:
                player = found[0]
                player.player_name = name
                player.active = True
                player.guild = guild # он мог быть в другой ги
        player.save()
    # убрать игроков которые уже не в ги
    for player in Player.filter(guild=guild):
        found = False
        for p in players:
            if p[0].attrib['href'][3:-1] == player.swgoh_name:
                found = True
                break
        if not found:
            player.active = False
            player.save()


def update_guilds():
    # Обновить данные по всем гильдиям
    for guild in Guild.objects.all():
        if guild.active:
            update_guild(guild)