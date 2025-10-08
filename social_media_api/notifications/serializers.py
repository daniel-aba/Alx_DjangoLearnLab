# notifications/serializers.py (NEW FILE in VS Code)
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    # Target details requires careful serialization due to GenericForeignKey, 
    # but for simplicity, we'll only display the target class and ID.
    target_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 'target_type', 'object_id', 'timestamp', 'read']
        read_only_fields = ['recipient', 'actor', 'verb', 'target_type', 'object_id', 'timestamp']