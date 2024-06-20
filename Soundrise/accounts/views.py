from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:success')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def profile(request, id):
    context = {
                'name': id,
              }
    
    return render(request, 'pages/profile.html', context)

def success(request):
    return render(request, 'pages/success.html')

def parametre(request):
    return render(request,'pages/parametre.html')

def parametre_about(request):
    return render(request,'pages/parametre/about.html')

def parametre_cookie(request):
    return render(request,'pages/parametre/cookie.html')

def parametre_confidentiality(request):
    return render(request,'pages/parametre/confidentiality.html')
