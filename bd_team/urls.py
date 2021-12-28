from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from example.views import MemberList

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('addplayer/', add_page_player, name='add_player'),
    path('listplayer/', ListPlayer.as_view(), name='list_players'),
    path('listgame/', ListChartGame.as_view(), name='list_game'),
    path('archivegame/', ListArchiveGame.as_view(), name='archive_game'),
    path('archivegame/<int:game_id>/', change_archive, name='add_archive'),
    path('player/<int:player_id>/', show_player_card, name='player'),
    path('update/<int:pk>/', PlayerUpdateView.as_view(), name='update_player'),
    path('delete/<int:pk>/', PlayerDeleteView.as_view(), name='delete_player'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('addgame/', GameCreateView.as_view(), name='add_game'),
    path('addinfogame/<int:game_id>/', add_game_info, name='add_game_info'),
    path('infogame/<int:game_id>/', game_info, name='game_info'),
    path('updategame/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('deletegame/<int:pk>/', GameDeleteView.as_view(), name='delete_game'),
    path('exportactivegame/exel/', export_exel_active_game, name='export_active_game_exel'),
    path('exportactivegame/json/', export_json_active_game, name='export_active_game_json'),
    path('exportaarchivegame/exel/', export_exel_archive_game, name='export_archive_game_exel'),
    path('exportarchivegame/json/', export_json_archive_game, name='export_archive_game_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
