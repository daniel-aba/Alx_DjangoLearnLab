# accounts/models.py (in VS Code)

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # 'following' is a ManyToMany field referencing itself.
    # related_name='followers' means: User.followers returns users who follow this user.
    # symmetrical=False is crucial for follow relationships.
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers', # users who follow this user
        blank=True
    )

    def __str__(self):
        return self.username

    # NOTE: If 'followers' field already exists, ensure it matches this setup.