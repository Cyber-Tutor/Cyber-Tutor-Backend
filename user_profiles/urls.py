from django.urls import path
from . import views

from user_profiles.forms import login_form

urlpatterns = [
    path('', views.index, name="index"),
    
    path('accounts/profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]