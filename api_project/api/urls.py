from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views # Add this line
from .views import BookViewSet

# Create a router instance
router = DefaultRouter()

# Register the ViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token), # Add this line
]