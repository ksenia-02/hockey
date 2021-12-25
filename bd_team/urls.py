from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
#from example.views import MemberList

urlpatterns = [
    path('', main_page, name = 'main_page'),
    path('addplayer/', add_page_player, name = 'add_player'),
    path('listplayer/', ListPlayer.as_view(), name = 'list_players'),
    path('listgame/',  ListChartGame.as_view(), name = 'list_game'),
    path('player/<int:player_id>', show_player_card, name='player'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)