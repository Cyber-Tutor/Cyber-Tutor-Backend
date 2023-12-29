from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from user_profiles.forms import register_form


def index(request):
    return render(request, 'base.html', context={'user': request.user})

def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = register_form()
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # Pass request and POST data to the form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()  # Create a new form for GET requests

    return render(request, 'authentication/login.html', {'form': form})
        
@login_required
def profile(request):
    return render(request, 'user_profiles/profile.html', {'user': request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
