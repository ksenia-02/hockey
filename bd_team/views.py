import json
import pandas as pd
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Spacer,KeepTogether,tables
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.units import inch,cm,mm
from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import fileName2FSEnc

from .forms import *
from .permission import *
from .DataMixin import *

class MainPage(DataMixin, LoginRequiredMixin, ListView):
    model = Player
    login_url = reverse_lazy('login')
    template_name = 'bd_team/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

# -------Work player -------

class AddPlayer(DataMixin, MyPermissionMixin, CreateView):
    raise_exception = False
    model = Player
    fields = '__all__'
    permission_required = 'bd_team.add_player'
    template_name = 'bd_team/add_player.html'
    success_url = reverse_lazy('list_players')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление игрока")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PlayerUpdateView(DataMixin, MyPermissionMixin, UpdateView):
    model = Player
    permission_required = 'bd_team.change_player'
    template_name = 'bd_team/update.html'
    form_class = PlayerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменение данных об игроке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PlayerDeleteView(DataMixin, MyPermissionMixin, DeleteView):
    model = Player
    permission_required = 'bd_team.delete_player'
    fields = '__all__'
    success_url = reverse_lazy('list_players')
    template_name = 'bd_team/delete.html'

@permission_required('bd_team.view_player')
def show_player_card(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = get_user_context()
    context['player'] = player
    context['title'] = 'Карточка игрока'
    return render(request, 'bd_team/card_player.html', context)


class ListPlayer(DataMixin, ListView):
    model = Player
    template_name = 'bd_team/players_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title= "Список игроков", head= ['Номер', 'Имя', 'Амплуа'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

# -------Work game -------

class GameCreateView(DataMixin, MyPermissionMixin, CreateView):
    model = Game
    permission_required = 'bd_team.add_game'
    template_name = 'bd_team/add_game.html'
    success_url = reverse_lazy('list_game')
    fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление матча")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class GameUpdateView(DataMixin, MyPermissionMixin, UpdateView):
    model = Player_Game
    permission_required = 'bd_team.change_game'
    template_name = 'bd_team/update.html'
    success_url = reverse_lazy('list_game')
    form_class = GamePlayerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title= "Изменение данных")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class GameDeleteView(DataMixin, MyPermissionMixin, DeleteView):
    model = Game
    permission_required = 'bd_team.delete_game'
    fields = '__all__'
    success_url = reverse_lazy('list_game')
    template_name = 'bd_team/delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Удаление матча")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ListChartGame(DataMixin, ListView):
    model = Game
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Расписание матчей",
                                      but = "Архивировать",
                                      head =['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья'],
                                      act=True)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Game.objects.filter(archive=False)


# -------Work game info -------

def game_info(request, game_id):
    p_game = Player_Game.objects.filter(game_id=game_id).order_by('-count_washers')
    if Player_Game.check_game_status(game_id):
        context = get_user_context()
        context['title'] = 'Состав игроков'
        context['p_game'] = p_game
        context['head'] = ['№', 'Игрок', 'Кол-во шайб', 'Желтая карточка', 'Красная карточка']
        return render(request, 'bd_team/info_game.html', context)
    else:
        return redirect('list_game')


@permission_required('bd_team.add_player_game')
def add_game_info(request, game_id):
    if Player_Game.check_game_status(game_id):
        if request.method == 'POST':
            form = GamePlayerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list_game')
        else:
            form = GamePlayerForm(initial={'game': game_id})
        context = get_user_context()
        context['game_id'] = game_id
        context['title'] = 'Добавление в состав игры'
        context['form'] = form
        return render(request, 'bd_team/add_game_info.html', context)
    else:
        return redirect('list_game')


# -------Work archive -------

class ListArchiveGame(DataMixin, MyPermissionMixin, ListView):
    model = Game.objects.filter(archive=True)
    permission_required = 'bd_team.view_game'
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Расписание матчей",
                                      but="Активировать",
                                      head =['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья'],
                                      act=False)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Game.objects.filter(archive=True)


#@permission_required('bd_team.change_game_player')
def change_archive(request, game_id):
    game = Game.objects.get(id=game_id)
    if game.archive:
        game.archive = False
    else:
        game.archive = True
    game.save()
    return redirect('list_game')


# -------User -------
def error(request):
    return render(request, 'bd_team/error.html', {})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bd_team/login.html'

    def get_success_url(self):
        return reverse_lazy('main_page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        context['but'] = "Войти"
        return context


def logout_user(request):
    logout(request)
    return redirect('login')


# -------Export -------

def export_exel_game(request, fl):
    game = Game.objects.filter(archive=fl).values()
    df = pd.DataFrame(game)
    if fl:
        df.to_excel('F:/file/game_archive.xlsx')
        return redirect('archive_game')
    else:
        df.to_excel('F:/file/game_active.xlsx')
        return redirect('list_game')


def export_json_game(request, fl):
    game = Game.objects.filter(archive=fl)
    game_json = serializers.serialize('json', game)
    if fl:
        with open('F:/file/game_archive.json', 'w') as f:
            f.write(json.dumps(game_json))
        return redirect('archive_game')
    else:
        with open('F:/file/game_active.json', 'w') as f:
            f.write(json.dumps(game_json))
        return redirect('list_game')


def export_pdf_game(request, fl):
    game = Game.objects.filter(archive=fl)
    styleSheet = getSampleStyleSheet()

    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))

    def StringGuy(text):
        return f'<font name="DejaVuSerif">{text}</font>'

    def ParagGuy(text, style=styleSheet['Normal']):
        return Paragraph(StringGuy(text), styleSheet['Normal'])

    data = [[ParagGuy('Дата'),
             ParagGuy('Соперник'),
             ParagGuy('Домашняя игра'),
             ParagGuy('Статус'),
             ParagGuy('Счет'),
             ParagGuy('Судья')]
            ]
    list = []

    for g in game:
        list.append(ParagGuy(g.date))
        list.append(ParagGuy(g.opponent))
        list.append(ParagGuy(g.area))
        list.append(ParagGuy(g.role))
        list.append(ParagGuy(g.score))
        data.append(list)
        list = []
    if fl:
        fileName = 'ArchiveGame.pdf'
    else:
        fileName = 'ActiveGame.pdf'

    pdf = SimpleDocTemplate(
        fileName,
        pagesize=letter
    )

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (6, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)

    table.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))
    elems = []
    elems.append(table)
    pdf.build(elems)
    if fl:
        return redirect('archive_game')
    else:
        return redirect('list_game')

# class RegisterUser(CreateView):
#    form_class = RegisterUserForm
#    template_name = 'bd_team/login.html'
#    success_url = reverse_lazy('login')

#    def get_context_data(self, *, object_list=None, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = "Добавление пользователя"
#        context['but'] = "Добавить"
#        return context
