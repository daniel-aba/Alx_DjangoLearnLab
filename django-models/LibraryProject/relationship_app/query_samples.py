import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# Import your models
from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Clean up any existing data for a fresh start
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()

    # 1. Create sample data
    author1 = Author.objects.create(name="Stephen King")
    author2 = Author.objects.create(name="J.K. Rowling")

    book1 = Book.objects.create(title="The Shining", author=author1)
    book2 = Book.objects.create(title="It", author=author1)
    book3 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author2)

    library1 = Library.objects.create(name="Central Library")
    library1.books.add(book1, book3)

    librarian1 = Librarian.objects.create(name="Jane Doe", library=library1)

    print("--- Sample Queries ---")

    # Query all books by a specific author
    king_books = Book.objects.filter(author__name="Stephen King")
    print("Books by Stephen King:")
    for book in king_books:
        print(f"- {book.title}")

    # List all books in a library
    central_library = Library.objects.get(name="Central Library")
    print(f"\nBooks in {central_library.name}:")
    for book in central_library.books.all():
        print(f"- {book.title}")

    # Retrieve the librarian for a library
    librarian_for_central_library = Librarian.objects.get(library=central_library)
    print(f"\nLibrarian for {central_library.name}:")
    print(f"- {librarian_for_central_library.name}")

if __name__ == "__main__":
    run_queries()