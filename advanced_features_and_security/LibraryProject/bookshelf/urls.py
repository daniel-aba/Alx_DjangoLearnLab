# bookshelf/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # CHANGE 1: Update the path to 'books/' and the view function to 'views.book_list'
    path('books/', views.book_list, name='book_list'),

    # CHANGE 2: Update the path and view function for the create view
    path('books/new/', views.book_create, name='book_create'),

    # CHANGE 3: Update the path and view function for the edit view
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),

    # CHANGE 4: Update the path and view function for the delete view
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]