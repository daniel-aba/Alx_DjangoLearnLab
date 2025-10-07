# social_media_api/urls.py (in VS Code)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # All API endpoints will be prefixed with 'api/'
    path('api/', include('accounts.urls')),
]