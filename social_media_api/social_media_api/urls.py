# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Existing accounts routes at /api/ (e.g., /api/register)
    path('api/', include('accounts.urls')),
    # New posts/comments routes at /api/ (e.g., /api/posts)
    path('api/', include('posts.urls')), 
]