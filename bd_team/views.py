from django.shortcuts import render, redirect
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
      form = AddPlayer(request.POST)
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

def post_list_players(request):
   players = Player.objects.all()
   context = {
      'title':'Игроки',
      'menu': menu,
      'players': players,
   }
   return render(request, 'bd_team/players_list.html', context)

class ListChartGame(ListView):
   model = Chart_Games
   template_name = 'bd_team/list_game.html'

   def get_context_data(self, *, object_list=None, **kwargs):
      context = super().get_context_data(**kwargs)
      context['menu'] = menu
      context['title'] = "Расписание игр"
      context['head'] = ['Дата', 'Соперник', 'Дом', 'Счёт']
      return context
