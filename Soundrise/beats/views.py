from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BeatForm

def upload_view(request):
    return HttpResponse("Welcome to the beats Page")

def upload_beat(request):
    if request.method == 'POST':
        form = BeatForm(request.POST, request.FILES)
        if form.is_valid():
            beat = form.save(commit=False)
            beat.artist = request.user  # == user
            beat.save()
            return redirect('accounts:profile')  # redirec
    else:
        form = BeatForm()
    
    return render(request, 'upload_beat.html', {'form': form})