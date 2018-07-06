from django.db import models


class Guild(models.Model):
    guild_id = models.IntegerField(default=0)      # идентификатор гильдии на swgoh.gg
    name = models.CharField(max_length=200)        # наименование гильдии
    active = models.BooleanField(default=True)     # требуется обновлять данные
    def __str__(self):
        return "%s [%d]" % (self.name, self.guild_id)


class Player(models.Model):
    # Данные для Телеграма
    chat_id = models.IntegerField(default=0)       # идентификатор в Телеграм
    user_name = models.CharField(max_length=200)   # ник в Телеграм
    first_name = models.CharField(max_length=200)  # отображаемое имя в Телеграм
    last_name = models.CharField(max_length=200)   # ---"---
    # Данные игры
    player_id = models.CharField(max_length=30)    # PlayerID из игры
    ally_code = models.CharField(max_length=11)    # код союзника из игры
    player_name = models.CharField(max_length=100) # игровое имя
    swgoh_name = models.CharField(max_length=100)  # имя пользователя swgoh.gg
    #
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)    # признак что пользователь активен
    def __str__(self):
        return "%s [%s]" % (self.player_name, self.guild.name)
    class Meta:
        ordering = ['player_name']

class Character(models.Model):
    base_id = models.CharField(max_length=200)     # код персонажа на swgoh.gg
    name = models.CharField(max_length=200)        # имя
    description = models.CharField(max_length=300) # описание
    combat_type = models.IntegerField(default=0)   # тип: 1 - персонаж, 2 - корабль
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
    category = models.CharField(max_length=50, choices=SQUAD_CATEGORY,default='other')
    char1 = models.ForeignKey(Character, related_name='char1', verbose_name='Character 1', blank=True, null=True, on_delete=models.SET_NULL)
    char2 = models.ForeignKey(Character, related_name='char2', verbose_name='Character 2', blank=True, null=True, on_delete=models.SET_NULL)
    char3 = models.ForeignKey(Character, related_name='char3', verbose_name='Character 3', blank=True, null=True, on_delete=models.SET_NULL)
    char4 = models.ForeignKey(Character, related_name='char4', verbose_name='Character 4', blank=True, null=True, on_delete=models.SET_NULL)
    char5 = models.ForeignKey(Character, related_name='char5', verbose_name='Character 5', blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return "%s - %s [%s, %s, %s, %s, %s]" % (self.name, self.category, self.char1, self.char2, self.char3, self.char4, self.char5)
    class Meta:
        ordering = ['name']

