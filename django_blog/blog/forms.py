from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post # Import the Post model

# (Keep your existing UserRegisterForm here)

# ⬅️ NEW: Post ModelForm for creation and updating
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Exclude 'author' and 'published_date' as they are set automatically
        fields = ['title', 'content']