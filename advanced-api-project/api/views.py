from rest_framework import generics
from rest_framework import permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to handle listing all books and creating a new one.

    - **GET:** Returns a list of all books.
    - **POST:** Creates a new book instance. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission class to allow read-only access for unauthenticated users
    # and full access (create, update, delete) only for authenticated users.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to handle retrieving, updating, and deleting a single book instance.
    
    - **GET:** Retrieves a single book by its primary key.
    - **PUT/PATCH:** Updates a book. Requires authentication.
    - **DELETE:** Deletes a book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Ensures only authenticated users can modify or delete a book.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]