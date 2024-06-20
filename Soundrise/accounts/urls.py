from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='other_profile'),
    path('success/', views.success, name='success'),
    path('parametre/', views.parametre, name='parametre'),
    path('parametre/about/', views.parametre_about, name='parametre_about'),
    path('parametre/cookie/', views.parametre_cookie, name='parametre_cookie'),
    path('parametre/confidentiality/', views.parametre_confidentiality, name='parametre_confidentiality'),
    path('recherhche/', views.recherche, name='recherhce'),

   
]