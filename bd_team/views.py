import json
import pandas as pd
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
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

menu = [{'title': "Игроки", 'url_name': 'list_players'},
        {'title': "Расписание матчей", 'url_name': 'list_game'},
        {'title': "Архив сыгранных матчей", 'url_name': 'archive_game'},
        {'title': "Выход", 'url_name': 'logout'},
        ]


# permission_player = ('bd_team.change_player', 'bd_team.view_game ', 'bd_team.view_player_game', 'bd_team.change_player',)
# permission_coach = ('bd_team.view_player', 'bd_team.view_game ', 'bd_team.view_player_game',
#                     'bd_team.add_player', 'bd_team.add_game ', 'bd_team.add_player_game',
#                    'bd_team.delete_player', 'bd_team.delete_game ', 'bd_team.delete_player_game',
#                     'bd_team.change_player', 'bd_team.change_game ', 'bd_team.change_player_game',)

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        player = Player.objects.all().order_by('role')
        return render(request, 'bd_team/main.html', {'menu': menu, 'title': 'Главная', 'player': player})


# -------Work player -------

class AddPlayer(PermissionRequiredMixin, CreateView):
    model = Player
    fields = '__all__'
    permission_required = 'bd_team.add_player'
    template_name = 'bd_team/add_player.html'
    success_url = reverse_lazy('players_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Добавление игрока"
        return context


# def add_page_player(request):
#    if request.user.has_perm('polls.can_add'):
#        if request.method == 'POST':
#            form = PlayerForm(request.POST, request.FILES)
#            if form.is_valid():
#                form.save()
#                return redirect('list_players')
#        else:
#            form = PlayerForm()
#        context = {
#            'title': 'Добавление игрока',
#            'menu': menu,
#            'form': form,
#        }
#        return render(request, 'bd_team/add_player.html', context)
#    else:
#        return render(request, 'bd_team/error.html')


class PlayerUpdateView(PermissionRequiredMixin, UpdateView):
    model = Player
    permission_required = 'bd_team.change_player'
    template_name = 'bd_team/update.html'
    form_class = PlayerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Изменение данных об игроке"
        return context


class PlayerDeleteView(PermissionRequiredMixin, DeleteView):
    model = Player
    permission_required = 'bd_team.delete_player'
    fields = '__all__'
    success_url = reverse_lazy('list_players')
    template_name = 'bd_team/delete.html'


def show_player_card(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {
        'title': 'Карточка игрока',
        'menu': menu,
        'player': player,
    }
    return render(request, 'bd_team/card_player.html', context)


class ListPlayer(ListView):
    model = Player
    template_name = 'bd_team/players_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Список игроков"
        context['head'] = ['Номер', 'Имя', 'Амплуа']
        return context


# -------Work game -------

class GameCreateView(PermissionRequiredMixin, CreateView):
    model = Game
    permission_required = 'bd_team.add_game'
    template_name = 'bd_team/add_game.html'
    success_url = reverse_lazy('list_game')
    fields = '__all__'


class GameUpdateView(PermissionRequiredMixin, UpdateView):
    model = Player_Game
    permission_required = 'bd_team.change_game'
    template_name = 'bd_team/update.html'
    success_url = reverse_lazy('list_game')
    form_class = GamePlayerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Изменение данных"
        return context

    def get_login_url(self):
        return 'error_access'


class GameDeleteView(PermissionRequiredMixin, DeleteView):
    model = Game
    permission_required = 'bd_team.delete_game'
    fields = '__all__'
    success_url = reverse_lazy('list_game')
    template_name = 'bd_team/delete.html'


class ListChartGame(ListView):
    model = Game
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Расписание игр"
        context['but'] = "Архивировать"
        context['act'] = True
        context['head'] = ['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья']
        return context

    def get_queryset(self):
        return Game.objects.filter(archive=False)


# -------Work game info -------

def game_info(request, game_id):
    p_game = Player_Game.objects.filter(game_id=game_id).order_by('-count_washers')
    if Player_Game.check_game_status(game_id):
        context = {
            'title': 'Состав игроков',
            'menu': menu,
            'p_game': p_game,
            'head': ['№', 'Игрок', 'Кол-во шайб', 'Желтая карточка', 'Красная карточка'],
        }
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
        context = {
            'game_id': game_id,
            'title': 'Добавление в состав игры',
            'menu': menu,
            'form': form,
        }
        return render(request, 'bd_team/add_game_info.html', context)
    else:
        return redirect('list_game')


# -------Work archive -------

class ListArchiveGame(PermissionRequiredMixin, ListView):
    model = Game.objects.filter(archive=True)
    permission_required = 'bd_team.view_game'
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Расписание игр"
        context['but'] = 'Активировать'
        context['act'] = False
        context['head'] = ['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья']
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


def export_exel_active_game(request):
    game = Game.objects.filter(archive=False).values()
    print(dict)
    df = pd.DataFrame(game)
    df.to_excel('F:/file/game_active.xlsx')
    return redirect('list_game')


def export_json_active_game(request):
    game = Game.objects.filter(archive=False)
    game_json = serializers.serialize('json', game)
    with open('F:/file/game_active.json', 'w') as f:
        f.write(json.dumps(game_json))
    return redirect('list_game')


def export_exel_archive_game(request):
    game = Game.objects.filter(archive=True).values()
    print(dict)
    df = pd.DataFrame(game)
    df.to_excel('F:/file/game_archive.xlsx')
    return redirect('archive_game')


def export_json_archive_game(request):
    game = Game.objects.filter(archive=True)
    game_json = serializers.serialize('json', game)
    with open('F:/file/game_archive.json', 'w') as f:
        f.write(json.dumps(game_json))
    return redirect('archive_game')
'''
def export_pdf_active_game(request):
    print(request.user.id)
    id = request.user.id

    income = get_table(id)

    context = {'array': income, 'name_column': ['Название', 'Сумма', 'Тип']}
    template_path = 'budget/pdfS.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
'''


def export_pdf_archive_game(request):
    with open('active_game.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response


def export_pdf_active_game(request):
    game = Game.objects.filter(archive=False)
    styleSheet = getSampleStyleSheet()

    pdfmetrics.registerFont(TTFont('DejaVuSerif', "F:/coursework/bd_team/DejaVuSerif.ttf", 'UTF-8'))

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
    fileName = 'Game.pdf'

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

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)
    elems = []
    elems.append(table)

    pdf.build(elems)
###########################################################################
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
