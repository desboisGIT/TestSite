from django.http import HttpResponse
from django.shortcuts import render, redirect

def profile_view(request):
    return HttpResponse("Welcome to the profile_view Page")

def sell(request):
    
    return render(request,'pages/sell.html')