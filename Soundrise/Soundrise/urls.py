from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('content/', include('content.urls')),
    path('beats/', include('beats.urls')),
    path('beatmakers/', include('beatmakers.urls')),
    path('accounts/', include('accounts.urls')),
]
