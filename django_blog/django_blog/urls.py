from django.contrib.auth import views as auth_views 
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    # If using Django's simple path mapping:
    # path('', include('django.contrib.auth.urls')), 

    # Map our custom app views
    path('', include('blog.urls')), # Include paths from blog/urls.py
]
