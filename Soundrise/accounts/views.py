import os, glob
from pathlib import Path
from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ParametreForm, ParametreProForm, RegisterForm
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from beats.models import Beats
from django.db.models import Q



BASE_DIR = Path(__file__).resolve().parent.parent

def login_view(request):
    error_message = ""
    register_form = RegisterForm()

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:success')  # Redirect to home page after login
        else:
            error_message = "Invalid username or password. Please try again."
            

    return render(request, 'pages/login.html', {'form': register_form, 'error_message': error_message})

def register_view(request):
    print(os.path.join(BASE_DIR, 'files', 'static/'))
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('accounts:index')  # Redirect to home page after registration
    return render(request, 'pages/register.html', {'form': register_form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def get_audio_file(beat):
    media_root = settings.MEDIA_ROOT
    beat_directory = os.path.join(media_root, 'audio', 'beats')
    audio_files = glob.glob(os.path.join(beat_directory, '*.mp3'))
    
    for file_path in audio_files:
        if os.path.basename(file_path) == os.path.basename(beat.audio_file.name):
            relative_path = os.path.relpath(file_path, media_root)
            return os.path.join(settings.MEDIA_URL, relative_path)
    
    return None

@login_required
def profile(request, username=None):
    if username is None:
        user = request.user  # Logged-in user's profile
    else:
        user = get_object_or_404(CustomUser, username=username)  # Profile of the user with given username
    
    uploaded_beats = Beats.objects.filter(artist=user)
    
    for beat in uploaded_beats:
        beat.audio_file_url = get_audio_file(beat)
    
    context = {
        'user_profile': user,
        'uploaded_beats': uploaded_beats,
    }
    
    return render(request, 'pages/profile.html', context)


def success(request):
    return render(request, 'pages/success.html')



def parametre_about(request):
    return render(request,'pages/parametre/about.html')

def parametre_cookie(request):
    return render(request,'pages/parametre/cookie.html')

def parametre_confidentiality(request):
    return render(request,'pages/parametre/confidentiality.html')

def recherche(request):
    return render(request,'pages/recherche.html')


@login_required
def parametre(request):
    if request.method == 'POST':
        form = ParametreForm(request.POST,instance=request.user)
        form2 = ParametreProForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
                  
        elif form2.is_valid():
            form2.save()

    return render(request, 'pages/parametre.html')


@login_required
def parametre_onglet(request, page):
    print('page URLis: pages/parametre/'+page+'.html')
    if page == 'tableau':
        user = request.user 
        uploaded_beats = Beats.objects.filter(artist=user)
        context = {'uploaded_beats':uploaded_beats}
    else:
        context = {}
    return render(request, 'pages/parametre/'+page+'.html', context)
    


def explore(request):
    search_term = request.GET.get('search')
    error = None
    filtered_models = Beats.objects.all()
    
    # Applying search filter
    if search_term:
        filtered_models = filtered_models.filter(title__icontains=search_term)
        if not filtered_models.exists():
            error = f"No beats corresponding to: {search_term}"
    else:
        search_term =""
    
    # Applying price filter
    cursor_price = request.GET.get('cursor_price')
    if cursor_price:
        filtered_models = filtered_models.filter(price__lte=cursor_price)
    
    # Applying genre filter
    genre = request.GET.get('genre')
    if genre:
        filtered_models = filtered_models.filter(genre=genre)
    
    # Applying artist filter
    artist = request.GET.get('artist')
    if artist:
        filtered_models = filtered_models.filter(artist__icontains=artist)
    
    # Applying release year filter
    release_year = request.GET.get('release_year')
    if release_year:
        filtered_models = filtered_models.filter(release_year=release_year)
    
    # Applying sort order
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'price':
        filtered_models = filtered_models.order_by('price')
    elif sort_by == 'date':
        filtered_models = filtered_models.order_by('release_date')
    elif sort_by == 'duration':
        filtered_models = filtered_models.order_by('duration')
    # Add more sorting options as needed
    
    # Handling descending order
    order = request.GET.get('order')
    if order == 'desc':
        filtered_models = filtered_models.reverse()
    
    # Get all unique artist names from the filtered beats
    artist_names = filtered_models.values_list('artist', flat=True).distinct()
    
    # Get user data for all these artists
    users = CustomUser.objects.filter(username__in=artist_names)
    user_dict = {user.username: {'user': user, 'rank': user.rank} for user in users}
    
    # Prepare audio file URLs
    for beat in filtered_models:
        beat.audio_file_url = get_audio_file(beat)  # Assuming get_audio_file is a function to get audio file URL
    
    context = {
        'beats': filtered_models,
        'search_term': search_term,
        'error': error,
        'user_dict': user_dict,
    }
    return render(request, 'pages/explore.html', context)






def search_beatmakers(request):
    search_term = request.GET.get('search')
    error = None
    filtered_models = CustomUser.objects.all()  # Default queryset with all beatmakers
    
    if search_term:
        # Filter the model list using the search term
        filtered_models = CustomUser.objects.filter(
            Q(username__icontains=search_term) 
        )
        
        if not filtered_models.exists():
            error = f"No beatmakers corresponding to: {search_term}"
            search_term =""
    else:
        search_term ="" 
    
    context = {
        'beatmakers': filtered_models,
        'search_term': search_term,
        'error': error,
    }
    
    return render(request, 'pages/search_beatmakers.html', context)

def detail_beat(request, beat_id):
    beat = get_object_or_404(Beats, id=beat_id)

    context = {
        'beat': beat,
    }

    return render(request, 'pages/detail_beat.html', context)