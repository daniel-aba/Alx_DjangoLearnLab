from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # ... other paths if any
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]