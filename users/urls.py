
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import *

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user')


    #URLs for Password reset
    #TODO: set up an email backend for the reset link to actually work.
    # path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset',),
    # path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done',),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
    # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete',),
]
