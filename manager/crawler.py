#!/usr/bin/env python3
import requests
import json
import lxml.html
import cssselect
import datetime
import shutil
import os.path
from django.db import connection
from .models import *


def update_image(image, base_url='http://swgoh.gg/static/img/assets/tex.charui_'):
    fname = "static/manager/images/" + image

    # проверить что картинка уже есть
    if os.path.isfile(fname):
        return False

    # обновить картинку
    with requests.get(base_url + image, stream=True) as response:
        if response.status_code == 200:
            with open(fname, 'wb') as f:
                response .raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            print("Сохранен значок " + image)
            return True
        else:
            print("Ошибка получения значка %s - %d" % (image, response.status_code))

    return False


def update_character_database():
    # загрузить базу данных персонажей
    print("Обновляю базу данных по персонажам и кораблям")
    response = requests.get('https://swgoh.gg/api/characters')
    json_data = response.json()
    char_added = 0
    ship_added = 0
    total_updated = 0

    for idx, c in enumerate(json_data):
        char, created = Character.objects.update_or_create(base_id=c['base_id'], defaults={'base_id': c['base_id'], 'name': c['name'],
            'power': c['power'], 'description': c['description'], 'url': c['url'], 'image': c['image'][40:], 'combat_type': c['combat_type']})
        update_image(char.image)
        if created:
            char_added = char_added + 1
        else:
            total_updated = total_updated + 1

    # загрузить базу данных кораблей
    response = requests.get('https://swgoh.gg/api/ships')
    json_data = response.json()
    for c in json_data:
        char, created = Character.objects.update_or_create(base_id=c['base_id'], defaults={'base_id': c['base_id'], 'name': c['name'],
            'power': c['power'], 'description': c['description'], 'url': c['url'], 'image': c['image'][40:], 'combat_type': c['combat_type']})
        update_image(char.image)
        if created:
            ship_added = ship_added + 1
        else:
            total_updated = total_updated + 1

    print("Обновление завершено. Новых персонажей - %d, новых кораблей - %d. Обновлено всего - %d" % (char_added, ship_added, total_updated))


#response = requests.get('https://swgoh.gg/api/guilds/34508/units')
#json_data = response.json()
#with open('units.json','w+') as file:
#    json.dump(json_data, file)

def update_guild(guild):
    # запрос в свгох
    print("Загрузка данных по складам гильдии %s" % guild)
    response = requests.get("https://swgoh.gg/api/guild/%d" % guild.guild_id)
    json_data = response.json()
    players = json_data['players']
    characters = Character.objects.all()
    count = len(players)

    guild_data = json_data['data']
    if (guild.name != guild_data['name']) or (guild.total_power != guild_data['galactic_power']) or (guild.members != guild_data['member_count']):
        guild.name = guild_data['name']
        guild.total_power = guild_data['galactic_power']
        guild.members = guild_data['member_count']
        guild.save()
    update_image(guild.image, 'http://swgoh.gg/static/img/assets/tex.guild_')

    print("Загрузка данных завершена, начинаю сопоставление, всего игроков для обновления - %d" % count)
    current = 0
    players_added = 0
    units_added = 0
    units_updated = 0
    # разбор полученных данных
    for p in players:
        current = current + 1
        units = []
        units_total = len(p['units'])

        # найти игрока
        found = Player.objects.filter(ally_code=p['data']['ally_code'])
        if len(found) == 0:
            player = Player(player_name=p['data']['name'], ally_code=p['data']['ally_code'], guild=guild, total_power=p['data']['galactic_power'], active=True)
            player.save()
            print('[%d/%d] Новый игрок %s, юнитов - %d' % (current, count, player.player_name, units_total))
            players_added = players_added + 1
        else:
            player = found[0]
            if (player.player_name != p['data']['name']) or (player.guild != guild) or not player.active or (player.total_power != p['data']['galactic_power']):
                player.player_name = p['data']['name']
                player.guild = guild
                player.active = True
                player.total_power = p['data']['galactic_power']
                player.save()
                print('[%d/%d] Обновлен игрок %s, юнитов - %d' % (current, count, player.player_name, units_total))
            else:
                print('[%d/%d] Игрок %s, юнитов - %d' % (current, count, player.player_name, units_total))
            # загрузить известные юниты этого игрока
            units = Unit.objects.filter(player=player)

        # перебрать всех юниты этого игрока
        for u in p['units']:
            # поискать юнит
            found = [unit for unit in units if unit.character.base_id == u['data']['base_id']]
            if found:
                unit = found[0]
                if (unit.gear_level != u['data']['gear_level']) or (unit.power != u['data']['power']) or (unit.level != u['data']['level']) or (unit.rarity != u['data']['rarity']):
                    unit.gear_level = u['data']['gear_level']
                    unit.power = u['data']['power']
                    unit.level = u['data']['level']
                    unit.rarity = u['data']['rarity']
                    units_updated = units_updated + 1
                    unit.save()
            else:
                foundchar = [char for char in characters if char.base_id == u['data']['base_id']]
                unit = Unit(character=foundchar[0], player=player, gear_level=u['data']['gear_level'],
                    power=u['data']['power'], level=u['data']['level'], rarity=u['data']['rarity'])
                units_added = units_added + 1
                unit.save()
    print("Обновление данных по складам гильдии %s завершено. Новых игроков %d. Юнитов добавлено %d, обновлено %d" % (guild, players_added, units_added, units_updated))

    # теперь исключить тех игроков которые не в гильдии уже
    print("Удаление отсутствующих игроков из гильдии %s" % guild)
    players2 = Player.objects.filter(guild=guild)
    players_removed = 0
    count = len(players2)
    current = 0
    for player in players2:
        current = current + 1
        # поискать в данных свгох
        found = [p for p in players if str(p['data']['ally_code']) == player.ally_code]
        if len(found) == 0:
            player.guild = None
            player.active = False
            player.save()
            print('[%d/%d] Игрок %s выбыл из гильдии' % (current, count, player.player_name))
            players_removed = players_removed + 1
    print("Обновление списка игроков гильдии %s завершено. Игроков удалено %d" % (guild, players_removed))



def update_squads_totals():
    # Обновить данные по пачкам
    guilds = Guild.objects.all()
    for squad in Squad.objects.all():
        squad.total_useful = 0
        for guild in guilds:
            if guild.active:
                data = squad.populate_units(guild)
                # Отфильтровать по мощи
                squad.total_useful = squad.total_useful + len([v for v in data.values() if v['useful']])
                # Обновить список полезных
                for row in data.values():
                    if row['useful'] and (row['player'] != None):
                        squad.players.add(row['player'])
                    elif row['player'] != None:
                        squad.players.remove(row['player'])
        squad.save()
        print("Обновлена пачка %s, всего полезных - %d" % (squad, squad.total_useful))


def get_week(date):
    """Возвращает первый день недели на указанную дату"""
    day_idx = date.weekday()
    monday = date - datetime.timedelta(days=day_idx)
    return datetime.datetime.date(monday)


def update_players_totals(guild):
    # Обновить счетчики по игрокам
    week = get_week(datetime.datetime.now())
    for player in Player.objects.filter(guild=guild):
        player.total_power = 0
        player.total_chars = 0
        for unit in Unit.objects.filter(player=player):
            player.total_power = player.total_power + unit.power
            player.total_chars = player.total_chars + 1
        player.total_useful = player.squad_set.count()
        print("Обновлена статистика по игроку %s - power = %d, chars = %d" % (player, player.total_power, player.total_chars))
        player.save()
        # теперь записать статистику
        found = PlayerStat.objects.filter(player=player, week=week)
        if found:
            stat = found[0]
            if (stat.total_power != player.total_power) or (stat.total_chars != player.total_chars):
                stat.total_power = player.total_power
                stat.total_chars = player.total_chars
                stat.save()
        else:
            stat = PlayerStat(player=player, week=week, total_power=player.total_power, total_chars=player.total_chars)
            stat.save()


def update_required_units():
    # Удалить планы на прокачку по тем юнитам, которые уже выполнены
    deleted = 0
    rows = RequiredUnit.objects.raw("""SELECT ru.id FROM manager_requiredunit ru JOIN manager_unit u
            ON ru.character_id = u.character_id AND ru.player_id = u.player_id
            WHERE ru.gear_level <= u.gear_level AND ru.rarity <= u.rarity""")
    for ru in rows:
        deleted = deleted + 1
        print(f"[{deleted}] Удаляю выполненный план прокачки {ru.player.player_name} - {ru.character.name}")
        ru.delete()
    total = RequiredUnit.objects.count()
    print(f"***** Удалено выполненных планов на прокачку: {deleted}. Осталось запланированно: {total}")


def update_guilds():
    # Обновить данные по всем гильдиям
    for guild in Guild.objects.all():
        if guild.active:
            print("***** Запущено обновление гильдии %s" % guild)
            update_guild(guild)
            update_players_totals(guild)
    print("***** Обновление отрядов")
    update_squads_totals()
    print("***** Обновление завершено")

