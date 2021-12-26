# Generated by Django 4.0 on 2021-12-26 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd_team', '0004_rename_chart_games_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='judge',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cудья'),
        ),
        migrations.AlterField(
            model_name='game',
            name='score',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Формат: 0:0', regex='\\d+:\\d+')], verbose_name='Счёт'),
        ),
    ]
