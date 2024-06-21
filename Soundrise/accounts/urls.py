from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='other_profile'),
    path('success/', views.success, name='success'),
    path('parametre/', views.parametre, name='parametre'),
    path('recherhche/', views.recherche, name='recherhce'),
    path('parametre/page/<str:page>/', views.parametre_onglet, name='parametre_onglet'),
    path('explore/',views.explore,name='explore')
    
    

   
]


