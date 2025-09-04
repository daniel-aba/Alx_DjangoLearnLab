# Test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required
from .forms import UserRegisterForm
from .models import Book, Library, UserProfile

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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Helper functions for the user_passes_test decorator
def is_admin(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False

# Role-based views
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# New views for permission-based actions
@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/confirm_delete.html', {'book': book})