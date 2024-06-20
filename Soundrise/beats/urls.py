from django.urls import path
from . import views

app_name = 'beats'

urlpatterns = [
    path('upload/', views.upload_view, name='upload_page'),
]
