from django.db import models
from datetime import date


class Guild(models.Model):
    guild_id = models.IntegerField(default=0)      # идентификатор гильдии на swgoh.gg
    name = models.CharField(max_length=200, default='')        # наименование гильдии
    url = models.CharField(max_length=200, default='')         # ссылка на свгох
    image = models.CharField(max_length=200, default='')       # значок гильдии
    members = models.IntegerField(default=0)                   # количество игроков
    total_power = models.IntegerField(default=0)               # общая ГМ
    active = models.BooleanField(default=True)     # требуется обновлять данные
    description = models.CharField(max_length=300, default='') # примечание
    def __str__(self):
        return "%s [%d]" % (self.name, self.guild_id)


class Player(models.Model):
    # Данные игры
    player_name = models.CharField(max_length=100)             # игровое имя
    ally_code = models.CharField(max_length=9, default='', blank=True)    # код союзника из игры
    player_id = models.CharField(max_length=30, default='', blank=True)    # PlayerID из игры
    #
    description = models.CharField(max_length=300, default='', blank=True) # примечание к игроку
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)                # признак что пользователь активен
    total_power = models.IntegerField(default=0)               # общая ГМ
    total_chars = models.IntegerField(default=0)               # всего персонажей на складе
    total_useful = models.IntegerField(default=0)              # количество годных пачек для ВГ
    # Данные для Телеграма
    chat_id = models.IntegerField(default=0)                   # идентификатор в Телеграм
    user_name = models.CharField(max_length=200, default='', blank=True)   # ник в Телеграм
    first_name = models.CharField(max_length=200, default='', blank=True)  # отображаемое имя в Телеграм
    last_name = models.CharField(max_length=200, default='', blank=True)   # ---"---
    def __str__(self):
        return "%s [%s]" % (self.player_name, self.guild.name if self.guild else '---')
    class Meta:
        ordering = ['player_name']

class Character(models.Model):
    base_id = models.CharField(max_length=200)     # код персонажа на swgoh.gg
    name = models.CharField(max_length=200)        # имя
    description = models.CharField(max_length=300) # описание
    COMBAT_TYPE = ((1, 'character'), (2, 'ship'))
    combat_type = models.IntegerField(choices=COMBAT_TYPE, default=1)   # тип: 1 - персонаж, 2 - корабль
    power = models.IntegerField(default=0)         # максимальная сила
    url = models.CharField(max_length=300)         # ссылка на swgoh.gg
    image = models.CharField(max_length=300)       # картинка на swgoh.gg
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class Unit(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    gear_level = models.IntegerField(default=0)    # уровень тира
    power = models.IntegerField(default=0)         # мощь персонажа
    level = models.IntegerField(default=0)         # уровень персонажа
    rarity = models.IntegerField(default=0)        # редкость персонажа
    def __str__(self):
        return "%s (%s)" % (self.character, self.player)
    class Meta:
        ordering = ['character__name']


class Squad(models.Model):
    name = models.CharField(max_length=200)
    SQUAD_CATEGORY = (
            ('other', 'Другое'),
            ('arena', 'Арена'),
            ('raid-rancor', 'Рейд: Ранкор'),
            ('raid-aat', 'Рейд: AAT'),
            ('raid-sith', 'Рейд: Триумвират ситхов'),
            ('lstb', 'Светлые территориальные битвы'),
            ('dstb', 'Темные территориальные битвы'),
            ('tw-offense', 'Войны гильдий: Атака'),
            ('tw-defense', 'Войны шильдий: Защита'),
        )
    category = models.CharField(max_length=50, choices=SQUAD_CATEGORY, default='other')
    description = models.TextField(blank=True)
    char1 = models.ForeignKey(Character, related_name='char1', verbose_name='Character 1', blank=True, null=True, on_delete=models.SET_NULL)
    char2 = models.ForeignKey(Character, related_name='char2', verbose_name='Character 2', blank=True, null=True, on_delete=models.SET_NULL)
    char3 = models.ForeignKey(Character, related_name='char3', verbose_name='Character 3', blank=True, null=True, on_delete=models.SET_NULL)
    char4 = models.ForeignKey(Character, related_name='char4', verbose_name='Character 4', blank=True, null=True, on_delete=models.SET_NULL)
    char5 = models.ForeignKey(Character, related_name='char5', verbose_name='Character 5', blank=True, null=True, on_delete=models.SET_NULL)
    total_useful = models.IntegerField(default=0)    # количество годных пачек для ВГ
    players = models.ManyToManyField(Player)         # список годных игроков

    def __str__(self):
        return "%s - %s [%s, %s, %s, %s, %s]" % (self.name, self.category, self.char1, self.char2, self.char3, self.char4, self.char5)

    def required_units(self):
        count = 0
        if self.char1:
            count = count + 1
        if self.char2:
            count = count + 1
        if self.char3:
            count = count + 1
        if self.char4:
            count = count + 1
        if self.char5:
            count = count + 1
        return count

    def _default_squad(self, player, can_require=False, required_units=[]):
        return {'squad': self, 'player': player,
                'char1': None, 'char1_require': can_require and not self.char1 in required_units, 'char1_useful': False,
                'char2': None, 'char2_require': can_require and not self.char2 in required_units, 'char2_useful': False,
                'char3': None, 'char3_require': can_require and not self.char3 in required_units, 'char3_useful': False,
                'char4': None, 'char4_require': can_require and not self.char4 in required_units, 'char4_useful': False,
                'char5': None, 'char5_require': can_require and not self.char5 in required_units, 'char5_useful': False,
                'power': 0, 'useful': False}

    def _populate_players(self, guild=None, player=None, can_require=False, required_units={}):
        data = {}
        if player:
            ru = [ru.character for ru in required_units[player]]
            data[player.id] = self._default_squad(player, can_require=can_require, required_units=ru)
        elif guild:
            for player in Player.objects.filter(guild=guild):#, active=True):
                if required_units.get(player):
                    ru = [ru.character for ru in required_units[player]]
                else:
                    ru = []
                data[player.id] = self._default_squad(player, can_require=can_require, required_units=ru)
        return data

    def _populate_units(self, character, idx, data, guild=None, player=None, can_require=False, required_units={}):
        if character == None:
            return data
        if player:
            units = Unit.objects.filter(character=character, player=player)
        elif guild:
            units = Unit.objects.filter(character=character, player__guild=guild)
        else:
            units = Unit.objects.filter(character=character)
        for unit in units:
            item = data.get(unit.player.id)
            if item == None:
                item = self._default_squad(unit.player, can_require=can_require, required_units=required_units)
                data[unit.player.id] = item
            item['char%d' % idx] = unit

            # Проверить что персонажа можно назначить в задания по прокачке
            if can_require and required_units.get(unit.player):
                ru = [ru for ru in required_units[unit.player] if ru.character == unit.character]
                if not len(ru):
                    item['char%d_require' % idx] = False
                else:
                    item['char%d_require' % idx] = (ru[0].rarity > unit.rarity) or (ru[0].gear_level > unit.gear_level)
            # вычислить готовность item['char%d_useful' % idx] = False
            item['power'] = item['power'] + unit.power
        return data

    def _check_raid(self, unit):
        if self.char1 and (not unit['char1'] or unit['char1'].rarity < 7):
            return False
        if self.char2 and (not unit['char2'] or unit['char2'].rarity < 7):
            return False
        if self.char3 and (not unit['char3'] or unit['char3'].rarity < 7):
            return False
        if self.char4 and (not unit['char4'] or unit['char4'].rarity < 7):
            return False
        if self.char5 and (not unit['char5'] or unit['char5'].rarity < 7):
            return False
        return True

    def _check_power(self, unit):
        if self.char1 and (not unit['char1'] or unit['char1'].power < 6000):
            return False
        if self.char2 and (not unit['char2'] or unit['char2'].power < 6000):
            return False
        if self.char3 and (not unit['char3'] or unit['char3'].power < 6000):
            return False
        if self.char4 and (not unit['char4'] or unit['char4'].power < 6000):
            return False
        if self.char5 and (not unit['char5'] or unit['char5'].power < 6000):
            return False
        return True

    def _check_required(self, unit):
        if self.char1 and not unit['char1'] :
            return False
        if self.char2 and not unit['char2']:
            return False
        if self.char3 and not unit['char3']:
            return False
        if self.char4 and not unit['char4']:
            return False
        if self.char5 and not unit['char5']:
            return False
        return True

    def populate_units(self, guild=None, player=None, can_require=False, required_units={}):
        data = self._populate_players(guild=guild, player=player, can_require=can_require, required_units=required_units)
        self._populate_units(self.char1, 1, data, guild=guild, player=player, can_require=can_require, required_units=required_units)
        self._populate_units(self.char2, 2, data, guild=guild, player=player, can_require=can_require, required_units=required_units)
        self._populate_units(self.char3, 3, data, guild=guild, player=player, can_require=can_require, required_units=required_units)
        self._populate_units(self.char4, 4, data, guild=guild, player=player, can_require=can_require, required_units=required_units)
        self._populate_units(self.char5, 5, data, guild=guild, player=player, can_require=can_require, required_units=required_units)
        # Проверить полезность
        for unit in data.values():
            if self.category == 'raid-rancor' or self.category == 'raid-aat' or self.category == 'raid-sith':
                unit['useful'] = self._check_raid(unit)
            elif self.category == 'tw-offense' or self.category == 'tw-defense':
                unit['useful'] = self._check_power(unit)
            else:
                unit['useful'] = self._check_required(unit)
        return data

    def count_useful_for_guild(self, guild):
        # подсчет количества полезных отрядов в гильдии
        self.total_useful_guild = self.players.filter(guild=guild).count()
        return self.total_useful_guild

    @classmethod
    def count_useful_for_player(player):
        # подсчет количества полезных отрядов для игрока
        return player.squad_set.all().count()

    class Meta:
        ordering = ['name']

# Планы на прокачку по игрокам
class RequiredUnit(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rarity = models.IntegerField(default=0)        # до какой звезды качать (если 0 - то хотя бы открыть)
    gear_level = models.IntegerField(default=0)    # до какого тира качать (если 0 - не имеет значения)
    def __str__(self):
        return "%s (%s)" % (self.character, self.player)
    class Meta:
        ordering = ['character__name']


# Еженедельная статистика по игрокам
class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)    # игрок
    week = models.DateField(default=date.today)                     # дата съема статистики
    total_energy = models.IntegerField(default=0)                   # сколько энки всего сдал игрок
    total_power = models.IntegerField(default=0)                    # общая ГМ
    total_chars = models.IntegerField(default=0)                    # всего персонажей на складе
    class Meta:
        unique_together = ('player','week',)
        ordering = ['-week', 'player__player_name']
    def __str__(self):
        return "%s @ %s - %d energy, %d power, %d chars" % (self.player.player_name if self.player else '---', self.week, self.total_energy, self.total_power, self.total_chars)
