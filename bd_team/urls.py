from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name = 'main_page'),
    path('add_player/', add_page_player, name = 'add_player'),
]
