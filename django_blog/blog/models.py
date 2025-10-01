from django.db import models
# Import Django's User model (recommended way)
from django.contrib.auth import get_user_model 

User = get_user_model() 

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

    # Optional: Define absolute URL for redirection after CRUD operations
    from django.urls import reverse
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