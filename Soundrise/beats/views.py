import os
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BeatForm
from django.contrib.auth.decorators import login_required
from .models import Beats

def upload_view(request):
    return HttpResponse("Welcome to the beats Page")

@login_required
def upload_beat(request):
    if request.method == 'POST':
        form = BeatForm(request.POST, request.FILES)
        if form.is_valid():
            beat = form.save(commit=False)
            beat.artist = request.user  # Set the artist to the logged-in user
            beat.save()
            return redirect('accounts:profile', username=request.user.username)  # Redirect to the user's profile
    else:
        form = BeatForm()
    
    return render(request, 'pages/upload_beat.html', {'form': form})
