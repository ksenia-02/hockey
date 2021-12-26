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
    path('player/<int:player_id>/', show_player_card, name='player'),
    path('update/<int:pk>/', PlayerUpdateView.as_view(), name = 'update_player'),
    path('delete/<int:pk>/', PlayerDeleteView.as_view(), name='delete_player'),

    path('addgame/', GameCreateView.as_view(), name='add_game'),
    path('updategame/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('deletegame/<int:pk>/', GameDeleteView.as_view(), name='delete_game')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)