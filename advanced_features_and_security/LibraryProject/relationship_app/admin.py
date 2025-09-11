# relationship_app/admin.py
from django.contrib import admin
from .models import Book, Author, Library, Librarian


# You can register your models here to make them visible in the Django admin interface.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)

# You should not have any CustomUser-related code here anymore.
# The CustomUser model and its admin class were moved to the bookshelf app.