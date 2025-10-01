from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment # <-- ADDED 'Comment' HERE

# Custom form to ensure email is handled during registration,
# though Django's User model doesn't require it to be unique by default.
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

# ⬅️ NEW: Post ModelForm for creation and updating
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Exclude 'author' and 'published_date' as they are set automatically
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'rows': 4, 
            'placeholder': 'Add your comment here...',
            'class': 'form-control' # Optional: for styling
        }
    ))

    class Meta:
        model = Comment
        fields = ['content']