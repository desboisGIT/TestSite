from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'beats'

urlpatterns = [
    path('upload/', views.upload_beat, name='upload_beat'),
]
