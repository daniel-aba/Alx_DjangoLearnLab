from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Paths from previous tasks
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    # New paths for authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # New paths for role-based views
    path('admin_page/', views.admin_view, name='admin_page'),
    path('librarian_page/', views.librarian_view, name='librarian_page'),
    path('member_page/', views.member_view, name='member_page'),
]
