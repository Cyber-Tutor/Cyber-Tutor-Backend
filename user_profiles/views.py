from django.shortcuts import render
from django.conf import settings


def register(request):
    return render(request, 'register.html', {})

