from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from app_users.forms import register_form
from app_users.forms import login_form

def index(request):
    return render(request, 'index.html', context={'user': request.user})

def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = register_form()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = login_form(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = login_form()
    return render(request, 'registration/login.html', {'form': form})
        
@login_required
def profile(request):
    return render(request, 'app_users/profile.html', {'user': request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')