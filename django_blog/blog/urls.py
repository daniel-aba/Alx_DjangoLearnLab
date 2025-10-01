from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='blog-home'), # Assuming a home view exists
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Add more paths as the project grows...
]