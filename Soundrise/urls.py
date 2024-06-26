from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('content/home/', permanent=True)),
    path('content/', include('content.urls')),
    path('beats/', include('beats.urls')),
    path('beatmakers/', include('beatmakers.urls')),
    path('accounts/', include('accounts.urls')),
]

#urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)