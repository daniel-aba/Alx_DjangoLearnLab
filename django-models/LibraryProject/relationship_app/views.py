# This is a test change to trigger another git status

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('login') # or any other page, like a home page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})