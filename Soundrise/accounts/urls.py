from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='upload_page'),
    path('register/', views.register, name='register'),
]
