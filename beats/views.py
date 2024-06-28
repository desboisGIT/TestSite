from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import BeatForm
from django.contrib.auth.decorators import login_required
from .models import Beats
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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



@csrf_exempt
@require_POST
@login_required
def update_views(request):
    print("it workkkkkkkkkkkkkkKKKK (like a child in a chinese factory)")
    beat_id = request.POST.get('beat_id')
    if beat_id:
        try:
            beat = Beats.objects.get(id=beat_id)
            user = request.user
            if beat.add_view(user):
                return JsonResponse({'success': True, 'views': beat.view_count})
            else:
                return JsonResponse({'success': False, 'error': 'User has already viewed this beat'})
        except Beats.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Beat not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid Beat ID'})
