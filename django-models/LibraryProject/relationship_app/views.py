from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# This view is for adding a new book. Only users with the 'can_add_book' permission can access it.
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        # Logic to handle adding the book goes here.
        # For example, create a new Book instance from form data.
        return redirect('book-list') # Redirect to a list of books after adding
    return render(request, 'add_book.html') # A template to display the form

# This view is for editing an existing book. Only users with the 'can_change_book' permission can access it.
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Logic to handle updating the book goes here.
        # For example, update the book instance with new form data.
        return redirect('book-list') # Redirect to a list of books after editing
    return render(request, 'edit_book.html', {'book': book}) # A template to display the form

# This view is for deleting a book. Only users with the 'can_delete_book' permission can access it.
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list') # Redirect to a list of books after deleting
    return render(request, 'delete_book.html', {'book': book}) # A template for confirmation