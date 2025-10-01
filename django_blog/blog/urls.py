from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ( # ⬅️ NEW: Import the CBVs
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # CRUD URLs
    path('', PostListView.as_view(), name='post-list'), # Home page list view
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # pk is the primary key of the Post object
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Authentication URLs (from previous task)
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]