# accounts/urls.py (in VS Code)
from django.urls import path
from . import views
from .views import UserProfileView

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]