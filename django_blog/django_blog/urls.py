from django.contrib import admin
from django.urls import path, include 
# from django.contrib.auth import views as auth_views # ⬅️ REMOVE this if no longer needed

urlpatterns = [
    path('admin/', admin.site.urls),

    # ⬅️ REMOVAL: Remove the explicit login/logout paths here:
    # path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # This single line now handles register, login, logout, and profile via blog/urls.py
    path('', include('blog.urls')), 
]