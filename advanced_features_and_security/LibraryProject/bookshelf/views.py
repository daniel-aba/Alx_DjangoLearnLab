# bookshelf/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book # CHANGE 1: Import the Book model
from .forms import BookForm # CHANGE 2: Import the BookForm

# --- Views that require specific permissions ---

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request): # CHANGE 3: Function name for clarity
    books = Book.objects.all() # CHANGE 4: Use Book model
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request): # CHANGE 5: Function name
    if request.method == 'POST':
        form = BookForm(request.POST) # CHANGE 6: Use BookForm
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user # CHANGE 7: Use new foreign key name
            book.save()
            return redirect('book_list') # CHANGE 8: Redirect to new URL name
    else:
        form = BookForm() # CHANGE 9: Use BookForm
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk): # CHANGE 10: Function name
    book = get_object_or_404(Book, pk=pk) # CHANGE 11: Use Book model
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book) # CHANGE 12: Use BookForm
        if form.is_valid():
            form.save()
            return redirect('book_list') # CHANGE 13: Redirect to new URL name
    else:
        form = BookForm(instance=book) # CHANGE 14: Use BookForm
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk): # CHANGE 15: Function name
    book = get_object_or_404(Book, pk=pk) # CHANGE 16: Use Book model
    if request.method == 'POST':
        book.delete()
        return redirect('book_list') # CHANGE 17: Redirect to new URL name
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})