from django.urls import path
from . import views

urlpatterns = [
    path('get_timer_turn/', views.get_timer_turn, name='get_timer_turn'),
]
