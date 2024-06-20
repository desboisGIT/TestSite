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
                return redirect('success')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def profile(request, id):
    context = {
                'name': id,
              }
    
    return render(request, 'pages/profile.html', context)

def success(request):
    return render(request, 'pages/success.html')

def parametre(request):
    return render(request,'pages/parametre.html')