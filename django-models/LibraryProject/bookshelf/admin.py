from django.contrib import admin
from .models import Book

# Register the Book model to make it visible in the admin interface
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')

# Unregister the default registration (if you had it) and register the model with the custom admin class
# admin.site.unregister(Book) # Use this if you want to be extra careful, but it's not needed if you only register once
admin.site.register(Book, BookAdmin)