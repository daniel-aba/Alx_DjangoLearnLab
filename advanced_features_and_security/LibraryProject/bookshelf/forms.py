# bookshelf/forms.py

from django import forms
from .models import Book # CHANGE: Import Book model

class BookForm(forms.ModelForm): # CHANGE: Class name for clarity
    class Meta:
        model = Book # CHANGE: Use Book model
        fields = ['title', 'author_name', 'published_date'] # CHANGE: Use new fields from your model    