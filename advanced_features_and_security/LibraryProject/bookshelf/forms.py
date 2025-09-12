# bookshelf/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_name', 'published_date']

# ADD THIS NEW FORM BELOW YOUR EXISTING CODE
class ExampleForm(forms.Form):
    # This field demonstrates how to securely handle text input from a user.
    # Django's form validation and handling of this field prevents common attacks like XSS.
    user_input = forms.CharField(label='Enter some text', max_length=255)