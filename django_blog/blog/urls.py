from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # ⬅️ NEW IMPORT

urlpatterns = [
    # path('', views.home, name='blog-home'), # Assuming a home view exists
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # ⬅️ FIX: Add the login URL here as required by the checker
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # We can also add logout here for consistency
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # Add more paths as the project grows...
]