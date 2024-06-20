from django.urls import path
from . import views

app_name = 'content'


urlpatterns = [
    path('home/', views.index, name='index'),
]
