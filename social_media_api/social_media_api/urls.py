# social_media_api/urls.py (Add to existing file in VS Code)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('notifications.urls')), # <-- Add this line
]