from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Status(models.Model):

    name = models.CharField(max_length=100, verbose_name='Статус игры')

    def __str__(self):
        return self.name

class Chart_Games(models.Model):

    date = models.DateField(null=True, verbose_name= 'Дата')
    opponent = models.CharField(max_length=100, null = True, verbose_name= 'Соперник')
    area = models.BooleanField(null = True, default=False, verbose_name='Домашняя игра')
    role = models.ForeignKey('Status', on_delete=models.PROTECT, null=False, verbose_name="Статус игры", default = 1)
    score = models.CharField(max_length=5, null = True, validators=[
        RegexValidator(
            regex=r'\d+:\d+',
            message='Формат: 0:0'
        )
    ], verbose_name='Счёт')

    class Meta():
        ordering = ['date']

    def __str__(self):
        return f"{self.id}"

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
    #slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player', kwargs={'player_id':self.pk})

class Player_Rating(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, null = False, verbose_name= 'Игрок')
    count_game = models.IntegerField(default = 0, verbose_name= 'Кол-во игр')
    count_washers = models.IntegerField(default = 0, verbose_name='Кол-во шайб')
    indicator = models.IntegerField(default = 0, verbose_name='Показатель')

    def __str__(self):
        return self.player