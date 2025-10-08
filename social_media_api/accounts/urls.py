# accounts/urls.py (Final Update)
from django.urls import path
from . import views
from .views import (
    UserProfileView, 
    registration_view, 
    login_view, 
    # New imports for the Class-Based Views
    FollowUserView, 
    UnfollowUserView 
) 

urlpatterns = [
    # Existing Function-Based Routes
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    
    # Existing Class-Based Route
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Updated Class-Based Follow/Unfollow Routes (using .as_view())
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'), 
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'), 
]