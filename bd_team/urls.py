from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name = 'main_page'),
    path('addplayer/', add_page_player, name = 'add_player'),
    path('listplayer/',  post_list_players, name = 'list_players'),
]
