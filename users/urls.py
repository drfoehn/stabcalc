
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import *

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
    path('dashboard/', views.user_dashboard, name="dashboard"),

]
