from django.shortcuts import render

from django.http import HttpResponse

def login(request):
    return HttpResponse("Welcome to the login Page")

def register(request):
    return render(request, 'pages/register.html')