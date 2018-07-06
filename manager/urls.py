from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>/', views.player, name='player'),
    path('squads/', views.squads, name='squads'),
    path('squad/<int:squad_id>/', views.squad, name='squad'),
]
