# This is a test change to trigger another git status

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Implement Function-based View
def list_books(request):
    """A function-based view to list all books."""
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)

# Implement Class-based View
class LibraryDetailView(DetailView):
    """A class-based view to display details for a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'