"""
    urls
"""
from django.contrib import admin
from django.urls import path

from app.views.users_view import register_page, create_admin, login_page, logout_user, home
from app.views.round_view import generate_next_round
from app.views.arenas_view import enter_result
from app.views.players_view import\
    delete_players,\
    update_player,\
    create_player,\
    my_players_list,\
    all_players_list
from app.views.tournaments_view import\
    create_tournament,\
    update_tournament,\
    tournaments_list,\
    all_tournaments_in_progress,\
    filtered_all_tournaments_in_progress,\
    filtered_tournaments_list,\
    tournaments_detail,\
    start_tournament,\
    delete_tournaments,\
    finish_tournaments

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_page, name='register'),
    path('create_admin/', create_admin, name='create_admin'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', home, name='home'),

    path('players/list/', my_players_list, name='my_players_list'),
    path('players/list/all/', all_players_list, name='all_players_list'),
    path('players/update/<int:pk>/', update_player, name="update_players"),
    path('players/add', create_player, name="create_players"),
    path('players/<int:pk>/delete/', delete_players, name="delete_players"),

    path('tournaments/add', create_tournament, name="create_tournaments"),
    path('tournaments/update/<int:pk>/', update_tournament, name="update_tournaments"),
    path('tournaments/list/<str:value>/', tournaments_list, name="tournaments_list"),
    path('tournaments/list_all_in_progress/',
         all_tournaments_in_progress,
         name="all_tournaments_in_progress"
         ),
    path('tournaments/filtred_list_all_in_progress/',
         filtered_all_tournaments_in_progress,
         name="filtered_all_tournaments_in_progress"
         ),
    path('tournaments/list/filtered/<str:value>',
         filtered_tournaments_list,
         name="filtered_tournaments_list"
         ),
    path('tournaments/detail/<slug:pk>/', tournaments_detail, name="tournaments_detail"),
    path('tournaments/start/<slug:pk>/', start_tournament, name="start_tournament"),
    path('tournaments/<int:pk>/delete/', delete_tournaments, name="delete_tournaments"),
    path('tournaments/<int:pk>/finish/', finish_tournaments, name="finish_tournaments"),

    path('rounds/generate_next/<int:pk>/', generate_next_round, name="generate_next_round"),

    path('arenas/set_result/<int:pk>/', enter_result, name="enter_result"),
]
