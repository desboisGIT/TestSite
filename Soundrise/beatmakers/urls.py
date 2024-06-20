from django.urls import path
from . import views

app_name = 'beatmakers'

urlpatterns = [
    path('profile/<str:profile_name>/', views.profile_view, name='profile_page'),
]
