from django.urls import path
from . import views

app_name = 'beatmakers'

urlpatterns = [
    path('sell/', views.sell, name='sell'),
]