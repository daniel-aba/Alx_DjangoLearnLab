# relationship_app/models.py
from django.conf import settings
from django.db import models

# Define the choices for user roles
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    publisher = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book"),
            ("can_change_book", "Can change an existing book"),
            ("can_delete_book", "Can delete a book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField('Book')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name