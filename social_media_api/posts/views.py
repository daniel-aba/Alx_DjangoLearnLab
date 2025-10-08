from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# Custom Pagination Class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    # Filtering and Searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']
    # filterset_fields = ['author'] 

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        # Note: The post ID must be passed in the request data, e.g., {'post': 1, 'content': '...'}
        serializer.save(author=self.request.user)

# --- NEW FEED VIEW (Variable Name Updated) ---

class FeedView(ListAPIView):
    """
    Returns a list of posts from users the current authenticated user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        user = self.request.user
        
        # Explicitly name the variable for the followed users as 'following_users'
        # This holds a queryset of User objects that the current user is following.
        following_users = user.following.all()

        # Filter posts where the author is in the list of 'following_users' and order them by creation date.
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')

        return queryset