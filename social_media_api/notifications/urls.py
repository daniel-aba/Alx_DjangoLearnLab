# notifications/urls.py (NEW FILE in VS Code)
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
# Route for /api/notifications/
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls 