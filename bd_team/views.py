from django.shortcuts import render
from .models import *

menu = ['Расписание игр', 'Карточка игрока', 'Рейтинг игроков']

def main_page(request):
   return render(request, 'bd_team/base.html', {'menu':menu})