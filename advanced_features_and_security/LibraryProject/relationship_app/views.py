from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Book, Library # Assuming you have a Library model

# New function to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# New class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'

# View for user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# View for the admin page
@permission_required('is_staff')
def admin_view(request):
    return render(request, 'admin_page.html', {})

# View for the librarian page
@permission_required('is_staff')
def librarian_view(request):
    return render(request, 'librarian_page.html', {})
    
# ADD THIS ENTIRE FUNCTION
@login_required
def member_view(request):
    return render(request, 'member_page.html', {})


# This view is for adding a new book.
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        # Logic to handle adding the book goes here.
        return redirect('book-list')
    return render(request, 'add_book.html')

# This view is for editing an existing book.
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Logic to handle updating the book goes here.
        return redirect('book-list')
    return render(request, 'edit_book.html', {'book': book})

# This view is for deleting a book.
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'delete_book.html', {'book': book})