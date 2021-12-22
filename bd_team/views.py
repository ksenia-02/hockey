from django.shortcuts import render, redirect
from .models import *
from .forms import *

menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']

def main_page(request):
   return render(request, 'bd_team/base.html', {'menu':menu})


def add_page_player(request):

   if request.method == 'POST':
      form = AddPlayer(request.POST)
      if form.is_valid():
         form.save()
         return redirect('main_page')
   else:
      form = AddPlayer()
   context = {
      'menu': menu,
      'form': form,
   }
   return render(request, 'bd_team/add_player.html', context)

