# posts/urls.py (in VS Code)
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
# Route for /api/posts/
router.register(r'posts', PostViewSet)
# Route for /api/comments/
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls