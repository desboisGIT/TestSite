from django.shortcuts import render

from django.http import HttpResponse

def login(request):
    return render(request, 'pages/register.html')

def register(request):
    return render(request, 'pages/register.html')

def logout(request):
    return render(request, 'pages/login.html')

def profile(request, id):
    context = {
                'name': id,
              }
    
    return render(request, 'pages/profile.html', context)

def success(request):
    return render(request, 'pages/success.html')