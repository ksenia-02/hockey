from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from .models import *
from .forms import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView

# menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']
menu = [{'title': "Игроки", 'url_name': 'list_players'},
        {'title': "Расписание матчей", 'url_name': 'list_game'},
        {'title': "Архив сыгранных матчей", 'url_name': 'archive_game'},
        #        {'title': "Статистика игроков", 'url_name': 'stat_player'},
        ]
m_a = [{'title': "Выйти", 'url_name': 'list_players'},]

def main_page(request):
    if not request.user.has_perm('auth.view_user'):
        return redirect('login')
    else:
        return render(request, 'bd_team/base.html', {'menu': menu, 'title': 'Главная'})


def add_page_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_players')
    else:
        form = PlayerForm()
    context = {
        'title': 'Добавление игрока',
        'menu': menu,
        'form': form,
    }
    return render(request, 'bd_team/add_player.html', context)


class PlayerUpdateView(UpdateView):
    model = Player
    template_name = 'bd_team/update_page_player.html'
    form_class = PlayerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Изменение данных об игроке"
        return context


class PlayerDeleteView(DeleteView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('list_players')
    template_name = 'bd_team/delete_player.html'


class GameCreateView(CreateView):
    model = Game
    template_name = 'bd_team/add_game.html'
    fields = '__all__'


class GameUpdateView(UpdateView):
    model = Game
    template_name = 'bd_team/update_game.html'
    success_url = reverse_lazy('list_game')
    form_class = GameForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Изменение данных об игре"
        return context


class GameDeleteView(DeleteView):
    model = Game
    fields = '__all__'
    success_url = reverse_lazy('list_game')
    template_name = 'bd_team/delete_game.html'


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


class ListChartGame(ListView):
    model = Game
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Расписание игр"
        context['but'] = "Архивировать"
        context['head'] = ['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья']
        return context

    def get_queryset(self):
        return Game.objects.filter(archive=False)

class ListArchiveGame(ListView):
    model = Game.objects.filter(archive=True)
    template_name = 'bd_team/list_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Расписание игр"
        context['but'] = 'Активировать'
        context['head'] = ['№', 'Дата', 'Соперник', 'Домашняя игра', 'Статус', 'Счёт', 'Судья']
        return context

    def get_queryset(self):
        return Game.objects.filter(archive=True)


def game_info(request, game_id):
    p_game =Player_Game.objects.filter(game_id=game_id).order_by('-count_washers')
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


class GamePlayerCreateView(CreateView):
    model = Player_Game
    template_name = 'bd_team/add_game_info.html'
    fields = ['player', 'count_washers', 'yellow_card', 'read_card']
    fields = '__all__'


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

def change_archive(request, game_id):
    game = Game.objects.get(id = game_id)
    if game.archive:
        game.archive = False
    else:
        game.archive = True
    game.save()
    return redirect('list_game')

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

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bd_team/login.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
         context = super().get_context_data(**kwargs)
         context['title'] = "Добавление пользователя"
         context['but'] = "Добавить"
         return context
