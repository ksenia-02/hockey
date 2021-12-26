from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import *
from .forms import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

#menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']
menu = [{'title': "Игроки", 'url_name': 'list_players'},
        {'title': "Расписание матчей", 'url_name': 'list_game'},
#        {'title': "Архив сыгранных матчей", 'url_name': 'archive_game'},
#        {'title': "Статистика игроков", 'url_name': 'stat_player'},
]

def main_page(request):
   return render(request, 'bd_team/base.html', {'menu':menu, 'title':'Главная'})

def add_page_player(request):

   if request.method == 'POST':
      form = PlayerForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('list_players')
   else:
      form = PlayerForm()
   context = {
      'title':'Добавление игрока',
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
   player = get_object_or_404(Player, pk = player_id)
   context = {
      'title':'Карточка игрока',
      'menu': menu,
      'player': player,
   }
   return render(request, 'bd_team/card_player.html', context)

def home(request):
   return render(request, 'home.html')

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
      context['head'] = ['Дата', 'Соперник','Домашняя игра', 'Статус', 'Счёт', 'Судья']
      return context

#   def get_queryset(self):
#       return Chart_Games.objects.filter(is_published=True)