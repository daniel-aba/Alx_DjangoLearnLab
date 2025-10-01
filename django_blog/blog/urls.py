from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ( 
    # ... existing Post CBVs ...
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    # ⬅️ NEW: Import Comment CBVs
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    # POST CRUD URLs
    path('', PostListView.as_view(), name='post-list'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # ⬅️ NEW: COMMENT CRUD URLs
    # Note: 'pk' here refers to the Post's ID (used for CommentCreateView)
    path('post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    # Note: 'comment_pk' here refers to the Comment's ID
    path('comment/<int:comment_pk>/update/', CommentUpdateView.as_view(), name='comment-update'), 
    path('comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Authentication URLs 
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]