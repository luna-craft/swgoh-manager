from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('character/<int:character_id>/', views.character, name='character'),
    path('players/', views.players, name='players'),
    path('player/<int:player_id>/', views.player, name='player'),
    path('squads/', views.squads, name='squads'),
    path('squad/<int:squad_id>/', views.squad, name='squad'),
    path('squad/<int:squad_id>/json', views.squad_json, name='squad_json'),
    path('require_unit/<int:player_id>/<int:character_id>', views.require_unit, name='require_unit'),
    path('rancor/', views.rancor, name='rancor'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
