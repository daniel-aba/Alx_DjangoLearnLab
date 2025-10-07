# posts/serializers.py (in VS Code)
from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # Read-only field to display the author's username
    author_username = serializers.ReadOnlyField(source='author.username')

    # Read-only count of comments
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # 'author' is read-only as it's set by the view based on the current user
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['author'] # Ensure 'author' is set automatically

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        # 'author' and 'post' are read-only; they will be set by the view.
        fields = ['id', 'post', 'post_title', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post'] # Ensure these are set automatically