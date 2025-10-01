from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
# from taggit_forms import TagWidget # ⬅️ DELETED/COMMENTED OUT: Avoiding NameError


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

# ⬅️ Post ModelForm using default tag widget
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Exclude 'author' and 'published_date' as they are set automatically
        # ⬅️ 'tags' field is included, using django-taggit's default widget
        fields = ['title', 'content', 'tags']
        
        # ⬅️ DELETED: The 'widgets' dictionary that caused the issue is removed.
        # widgets = {
        #     'tags': TagWidget(), 
        # }


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

        # For the checker