from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from example.views import MemberList

urlpatterns = [
    path('', main_page, name='main_page'),

    # -------User-------
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # path('register/', RegisterUser.as_view(), name='register'),
    path('erroraccess/', error, name = 'error_access'),

    # -------Player-------
    path('addplayer/', AddPlayer.as_view(), name='add_player'),
    path('listplayer/', ListPlayer.as_view(), name='list_players'),
    path('player/<int:player_id>/', show_player_card, name='player'),
    path('update/<int:pk>/', PlayerUpdateView.as_view(), name='update_player'),
    path('delete/<int:pk>/', PlayerDeleteView.as_view(), name='delete_player'),

    # -------Game-------
    path('listgame/', ListChartGame.as_view(), name='list_game'),
    path('addgame/', GameCreateView.as_view(), name='add_game'),
    path('updategame/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('deletegame/<int:pk>/', GameDeleteView.as_view(), name='delete_game'),

    # -------Archive-------
    path('archivegame/', ListArchiveGame.as_view(), name='archive_game'),
    path('archivegame/<int:game_id>/', change_archive, name='add_archive'),

    # -------Info Game-------
    path('addinfogame/<int:game_id>/', add_game_info, name='add_game_info'),
    path('infogame/<int:game_id>/', game_info, name='game_info'),

    # -------Export-------
    path('exportactivegame/exel/', export_exel_active_game, name='export_active_game_exel'),
    path('exportactivegame/json/', export_json_active_game, name='export_active_game_json'),
    path('exportactivegame/pdf/', export_pdf_active_game, name='export_active_game_pdf'),
    path('exportaarchivegame/exel/', export_exel_archive_game, name='export_archive_game_exel'),
    path('exportarchivegame/json/', export_json_archive_game, name='export_archive_game_json'),
    path('exportarchivegame/pdf/', export_pdf_archive_game, name='export_archive_game_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
