# Generated by Django 2.0.6 on 2018-07-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_requiredunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='total_useful',
            field=models.IntegerField(default=0),
        ),
    ]