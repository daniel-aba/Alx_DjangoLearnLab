# accounts/urls.py (Updated)
from django.urls import path
from . import views
# Note: Importing registration_view and login_view is redundant if using 'from . import views'
# but is harmless. We'll stick to the clearest structure.
from .views import UserProfileView, registration_view, login_view 

urlpatterns = [
    # Existing routes
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    # Assuming UserProfileView is an APIView (it uses .as_view())
    path('profile/', UserProfileView.as_view(), name='profile'),

    # New follow routes
    # These paths require an integer ID in the URL to specify the target user
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]