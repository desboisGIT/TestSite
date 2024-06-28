import os, glob
from pathlib import Path
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ParametreForm, ParametreProForm, RegisterForm
from accounts.models import CustomUser
from transaction.forms import CompteBancaireForm , PayPalAccountForm
from django.contrib.auth.decorators import login_required
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
            return redirect('content/home/', permanent=True)
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
    is_followed = user.is_followed_by_user(request.user)
    follower_count = user.get_follower_count()
    following_count = user.get_following_count()
    
    context = {
        'user_profile': user,
        'uploaded_beats': uploaded_beats,
        'is_followed': is_followed,
        'follower_count': follower_count,
        'following_count':following_count,
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
    if search_term is None:
        search_term = ""
    error = None
    filtered_models = Beats.objects.all()
    resetButton = False
    
    # Applying search filter
    if search_term:
        filtered_models = filtered_models.filter(title__icontains=search_term)
        if not filtered_models.exists():
            error = f"No beats corresponding to: {search_term}"
    
    # Applying price filter
    cursor_price = request.GET.get('cursor_price')
    if cursor_price:
        filtered_models = filtered_models.filter(price__lte=cursor_price)
        resetButton = True
    
    # Applying genre filter
    genre = request.GET.get('genre')
    if genre:
        filtered_models = filtered_models.filter(genre__icontains=genre)
        resetButton = True
    
    # Applying artist filter
    artist = request.GET.get('artist')
    if artist:
        filtered_models = filtered_models.filter(artist__username__icontains=artist)
        resetButton = True
    
    # Applying release year filter
    release_date = request.GET.get('release_date')
    if release_date:
        filtered_models = filtered_models.filter(release_date=release_date)
        resetButton = True
    
    # Applying sort order
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'trending':
        filtered_models = filtered_models.order_by('-score')
        resetButton = True
    if sort_by == 'price':
        filtered_models = filtered_models.order_by('-price')
        resetButton = True
    elif sort_by == 'price (reversed)':
        filtered_models = filtered_models.order_by('price')
        resetButton = True
    elif sort_by == 'latest':
        filtered_models = filtered_models.order_by('-release_date')
        resetButton = True
    elif sort_by == 'oldest':
        filtered_models = filtered_models.order_by('release_date')
        resetButton = True
    # Add more sorting options as needed
    
    # Handling descending order
    order = request.GET.get('order')
    if order == 'desc':
        filtered_models = filtered_models.reverse()
    
    # Handle like/unlike button form submissions
    if request.method == 'POST':
        if request.user.is_authenticated:
            beat_id = request.POST.get('beat_id')  # Assuming you have a hidden input in the form with beat_id
            beat = get_object_or_404(Beats, id=beat_id)
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in
    
    # Get all unique artist names from the filtered beats
    artist_ids = filtered_models.values_list('artist', flat=True).distinct()
    
    # Get user data for all these artists
    users = CustomUser.objects.filter(id__in=artist_ids)
    user_dict = {user.username: {'user': user, 'rank': user.rank} for user in users}
    
    # Prepare audio file URLs
    for beat in filtered_models:
        beat.audio_file_url = get_audio_file(beat)  # Assuming get_audio_file is a function to get audio file URL
    
    top_3_beats = sorted(filtered_models, key=lambda b: b.score, reverse=True)[:3]
    top_3_scores = [beat.score for beat in top_3_beats]

    context = {
        'beats': filtered_models,
        'search_term': search_term,
        'error': error,
        'user_dict': user_dict,
        'sort_by': sort_by,
        'genre': genre,
        'artist': artist,
        'release_date': release_date,
        'resetButton': resetButton,
        'top_3_scores':top_3_scores,
    }
    
    return render(request, 'pages/explore.html', context)


@login_required
def toggle_follow(request, user_id, beat_id):
    if beat_id == 0:
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        
        # Logic to toggle follow/unfollow
        if current_user in user_to_follow.followers.all():
            user_to_follow.followers.remove(current_user)
        else:
            user_to_follow.followers.add(current_user)
        
        # Redirect back to the detail_beat page with the correct beat_id
        return redirect('accounts:profile', username=user_to_follow.username)
    
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user
    
    # Logic to toggle follow/unfollow
    if current_user in user_to_follow.followers.all():
        user_to_follow.followers.remove(current_user)
    else:
        user_to_follow.followers.add(current_user)
    
    # Redirect back to the detail_beat page with the correct beat_id
    return redirect('accounts:detail_beat', beat_id=beat_id)


def search_beatmakers(request):
    user = request.user
    is_followed = user.is_followed_by_user(request.user)
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
            search_term = ""
    else:
        search_term = ""

    # Add logic to fetch beats for each beatmaker
    annotated_models = []
    
    for beatmaker in filtered_models:
        # Use related_name 'uploaded_beats' defined in Beats model
        beats = beatmaker.uploaded_beats.all()
        for beat in beats:
            beat.audio_file_url = get_audio_file(beat)
        annotated_models.append({
            'beatmaker': beatmaker,
            'beats': beats,
            
        })
    
    context = {
        'annotated_models': annotated_models,  # Use annotated_models instead of beatmakers
        'search_term': search_term,
        'error': error,
        'beatmakers': filtered_models,
        'is_followed':is_followed,
    }

    return render(request, 'pages/search_beatmakers.html', context)


def detail_beat(request, beat_id):
    beat = get_object_or_404(Beats, id=beat_id)
    user = beat.artist
    is_followed = user.is_followed_by_user(request.user)
    follower_count = user.get_follower_count()
    following_count = user.get_following_count()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    # Handle successful like addition
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in

    context = {
        'beat': beat,
        'user': user,
        'is_followed': is_followed,
        'follower_count': follower_count,
        'following_count': following_count,
    }

    return render(request, 'pages/detail_beat.html', context)

def parametre_tableau(request):
    user = request.user
    uploaded_beats = Beats.objects.filter(artist=user)
    latest_model = uploaded_beats.latest('release_date')
    context = {
        'user':user,
        'latest_model':latest_model,
        
    }

    return render(request, 'pages/parametre/tableau', context)
    
def parametre_default(request):
    user = request.user
    follower_count = user.get_follower_count()
    context={
        'follower_count':follower_count,
    }
    return render(request, 'pages/parametre/default', context)

def create_card(request):
    return render(request, 'pages/create_card.html')
def parametre_transaction(request):
    return render(request, 'pages/parametre/transaction.html')


def parametre_like(request):
    user = request.user

    user_likes = []  # Initialize an empty list to store liked beats

    if user.is_authenticated:
        user_likes = Beats.objects.filter(likes=user)
    

    if request.method == 'POST':
        if request.user.is_authenticated:
            beat_id = request.POST.get('beat_id')  # Assuming you have a hidden input in the form with beat_id
            beat = get_object_or_404(Beats, id=beat_id)
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in

    context = {
        'user': user,
        'user_likes': user_likes,
    }

    return render(request, 'pages/parametre/activite-beat.html', context)
def parametre_fav(request):
    user=request.user
    beats=Beats.objects.all()
    favs=None
    for beat in beats :
        if user.has_fav():
            favs.append(beat)
        else:
            pass
    context = {
            'user':user,
            'fav':favs,

        }

                
    return render(request,'pages/parametre/activite-fav.html',context)
def parametre_com(request):
    return render(request,'pages/parametre/activite-com.html')

def historique_beat(request):
     return render(request,'pages/parametre/historique-beat.html')
def historique_artist(request):
     return render(request,'pages/parametre/historique-artist.html')
def historique_recherche(request):
     return render(request,'pages/parametre/historique-recherche.html')


def create_card(request):
    if not request.user.is_authenticated:
        return redirect('login_views')  # Redirect to login if not authenticated

    compte_bancaire_form = CompteBancaireForm(request.POST or None)
    paypal_account_form = PayPalAccountForm(request.POST or None)

    if compte_bancaire_form.is_valid():
        # Save Compte Bancaire form
        compte_bancaire = compte_bancaire_form.save(commit=False)
        compte_bancaire.user = request.user
        compte_bancaire.save()

        # Redirect to specific success page for Compte Bancaire
        return redirect('accounts:parametre_transaction')

    elif paypal_account_form.is_valid():
        # Save PayPal account form
        paypal_account = paypal_account_form.save(commit=False)
        paypal_account.user = request.user
        paypal_account.save()

        # Redirect to specific success page for PayPal account
        return redirect('accounts:parametre_transaction')

    else:
        # Handle invalid forms
        context = {
            'compte_bancaire_form': compte_bancaire_form,
            'paypal_account_form': paypal_account_form,
        }
        return render(request, 'pages/create_card.html', context)