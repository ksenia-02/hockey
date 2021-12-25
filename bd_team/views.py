from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import ListView

#menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']
menu = [{'title': "Добавить игрока", 'url_name': 'add_player'},
        {'title': "Игроки", 'url_name': 'list_players'},
        {'title': "Расписание игр", 'url_name': 'list_game'},
]

def main_page(request):
   return render(request, 'bd_team/base.html', {'menu':menu, 'title':'Главная'})

def add_page_player(request):

   if request.method == 'POST':
      form = AddPlayer(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('main_page')
   else:
      form = AddPlayer()
   context = {
      'title':'Добавление игрока',
      'menu': menu,
      'form': form,
   }
   return render(request, 'bd_team/add_player.html', context)

def show_player_card(request, player_id):
   player = get_object_or_404(Player, pk = player_id )
   context = {
      'title':'Карточка игрока',
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
   model = Chart_Games
   template_name = 'bd_team/list_game.html'

   def get_context_data(self, *, object_list=None, **kwargs):
      context = super().get_context_data(**kwargs)
      context['menu'] = menu
      context['title'] = "Расписание игр"
      context['head'] = ['', '']
      return context

#   def get_queryset(self):
#       return Chart_Games.objects.filter(is_published=True)