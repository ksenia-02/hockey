from django.contrib.auth.models import User, AbstractUser, Group
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус игры')

    def __str__(self):
        return self.name

    def ch(self):
        return self.id == 1


class Game(models.Model):
    date = models.DateField(null=True, verbose_name='Дата')
    opponent = models.CharField(max_length=100, null=True, verbose_name='Соперник')
    area = models.BooleanField(null=True, default=False, verbose_name='Домашняя игра')
    role = models.ForeignKey('Status', on_delete=models.PROTECT, null=False, verbose_name="Статус игры", default=1)
    score = models.CharField(max_length=5, null=True, blank=True, validators=[
        RegexValidator(
            regex=r'\d+:\d+',
            message='Формат: 0:0'
        )
    ], verbose_name='Счёт')
    judge = models.CharField(max_length=100, null=True, blank=True, verbose_name='Cудья')
    archive = models.BooleanField(default=False, verbose_name='Архив')

    class Meta():
        ordering = ['date']

    def __str__(self):
        return f"{self.id}.{self.opponent}_{self.date}"

    def get_absolute_url(self):
        return reverse('game_info', kwargs={'game_id': self.pk})

    def check_status(self):
        return Status.objects.get(name=self.role).ch()


class Category_Player(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Амплуа')

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name="ФИО")
    date_birth = models.DateField(null=True, verbose_name="Дата рождения")
    citizenship = models.CharField(max_length=100, null=True, verbose_name="Гражданство")
    role = models.ForeignKey('Category_Player', on_delete=models.PROTECT, null=True, verbose_name="Амплуа")
    number = models.IntegerField(null=False, unique=True, verbose_name="Номер")
    photo = models.ImageField(null=True,blank = True,  upload_to="photos/", verbose_name="Фото")
    base = models.BooleanField(default=False, verbose_name='Основа')
    indicator = models.IntegerField(default=0, verbose_name='Показатель')
    biog = models.TextField(null = True, blank = True, verbose_name='Отображаемая информация')
    public_photo = models.ImageField(null=True, blank=True, upload_to="photos/", verbose_name="Публичное Фото")

    class Meta():
        ordering = ['number']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player', kwargs={'player_id': self.pk})


class Player_Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False, verbose_name='Игрок')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Игра')
    count_washers = models.IntegerField(default=0, verbose_name='Кол-во шайб')
    yellow_card = models.IntegerField(default=0, verbose_name='Жёлтая карточка')
    read_card = models.IntegerField(default=0, verbose_name='Красная карточка')

    class Meta():
        unique_together = ('player', 'game',)

    def __str__(self):
        return f"{self.player}:{self.game}"

    def get_absolute_url(self):
        return reverse('list_game', kwargs={})

    @staticmethod
    def check_game_status(id_game):
        game = Game.objects.get(id=id_game)
        print(game.check_status())
        return game.check_status()

