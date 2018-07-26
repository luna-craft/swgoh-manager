# Generated by Django 2.0.6 on 2018-07-20 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_guild_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guild',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='player',
            name='ally_code',
            field=models.CharField(default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='player',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='player',
            name='swgoh_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='player',
            name='user_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]