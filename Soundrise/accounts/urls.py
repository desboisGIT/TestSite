from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('success/', views.success, name='success'),
    path('parametre/', views.parametre, name='parametre'),
    path('parametre/about/', views.parametre, name='parametre'),
    path('parametre/cookie/', views.parametre, name='parametre'),
     path('parametre/confidentiality/', views.parametre, name='parametre'),
    
]