# notifications/views.py (NEW FILE in VS Code)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show notifications where the current user is the recipient
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Marks all unread notifications for the user as read."""
        count = self.get_queryset().filter(read=False).update(read=True)
        return Response({'message': f'Marked {count} notifications as read.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marks a single notification as read."""
        notification = self.get_object()
        if not notification.read:
            notification.read = True
            notification.save()
        return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)