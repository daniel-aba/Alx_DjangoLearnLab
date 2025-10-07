# posts/views.py (in VS Code)
from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
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
    # filterset_fields = ['author'] # Example of filtering by author ID

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