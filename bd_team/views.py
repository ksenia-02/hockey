from django.shortcuts import render, redirect
from .models import *
from .forms import *

#menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']
menu = [{'title': "Добавить игрока", 'url_name': 'add_player'},
        {'title': "Игроки", 'url_name': 'list_players'},
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
