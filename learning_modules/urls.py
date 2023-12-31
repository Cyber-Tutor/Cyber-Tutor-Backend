from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('content/', views.content, name='content'),

]