from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.utils import timezone

class Chart_Games(models.Model):

    date = models.DateField(null=True, verbose_name= 'Дата')
    opponent = models.CharField(max_length=100, null = True, verbose_name= 'Соперник')
    area = models.BooleanField(null = True, default=False, verbose_name='Домашняя игра')
    score = models.CharField(max_length=5, validators=[
        RegexValidator(
            regex=r'\d+:\d+',
            message='Формат: 0:0'
        )
    ], verbose_name='Счёт')

    def __str__(self):
        return self.name

class Category_Player(models.Model):

    name = models.CharField(max_length=100, db_index=True, verbose_name='Амплуа')

    def __str__(self):
        return self.name

class Player(models.Model):

    name = models.CharField(max_length=100, null = False, verbose_name= "ФИО")
    date_birth = models.DateField(null = True, verbose_name="Дата рождения")
    citizenship = models.CharField(max_length= 100, null = True, verbose_name="Гражданство")
    role = models.ForeignKey('Category_Player', on_delete=models.PROTECT, null = True, verbose_name="Амплуа")
    number = models.IntegerField(null = False,  unique = True, verbose_name = "Номер")
    photo = models.ImageField(null = True)

    def __str__(self):
        return self.name

class Player_Rating(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, null = False, verbose_name= 'Игрок')
    count_game = models.IntegerField(default = 0, verbose_name= 'Кол-во игр')
    count_washers = models.IntegerField(default = 0, verbose_name='Кол-во шайб')
    indicator = models.IntegerField(default = 0, verbose_name='Показатель')

    def __str__(self):
        return self.player