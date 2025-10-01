from django.db import models
from django.contrib.auth import get_user_model 
from django.urls import reverse
from taggit.managers import TaggableManager # ⬅️ NEW: Import Tag Manager

User = get_user_model() 

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    # ⬅️ NEW: Tags field
    tags = TaggableManager() 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# ⬅️ NEW: Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # ⬅️ Automatically updates on save

    class Meta:
        ordering = ['created_at'] # Display newest comments last (default order)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}'

    def get_absolute_url(self):
        # Redirect back to the post detail page after comment submission/edit
        return reverse('post-detail', kwargs={'pk': self.post.pk})