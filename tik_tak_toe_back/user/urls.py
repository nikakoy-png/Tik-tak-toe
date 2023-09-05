from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('get_user/<int:user_id>/', views.get_user, name='get_user'),
    path('get_user_order_by_rating/', views.get_users_order_by_rating, name='get_user_order_by_rating')
]
