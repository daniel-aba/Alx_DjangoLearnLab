# accounts/views.py (Updated)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# *** New Import: For 404 handling in follow/unfollow ***
from django.shortcuts import get_object_or_404 
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated # IsAuthenticated added

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() # This triggers the serializer's create method, which creates the user AND the token
        
        # The token has already been created, so we retrieve it to return it.
        token = Token.objects.get(user=user) 
        
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Simple profile view (for future use/testing)
from rest_framework.generics import RetrieveUpdateAPIView

class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer # Reusing registration serializer for simplicity
    permission_classes = [IsAuthenticated]
    # Only allow authenticated users to see their own profile
    def get_object(self):
        return self.request.user

# --- Social Endpoints ---

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Allows the authenticated user to follow another user by ID."""
    # The user to be followed
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Cannot follow self
    if current_user.id == target_user.id:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if already following
    if current_user.following.filter(id=target_user.id).exists():
        return Response({"detail": f"You are already following {target_user.username}."}, status=status.HTTP_200_OK)

    # Add the target user to the current user's 'following' list (ManyToManyField)
    current_user.following.add(target_user)
    return Response({"detail": f"Successfully followed {target_user.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """Allows the authenticated user to unfollow another user by ID."""
    # The user to be unfollowed
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Check if currently following
    if not current_user.following.filter(id=target_user.id).exists():
        return Response({"detail": f"You are not following {target_user.username}."}, status=status.HTTP_200_OK)

    # Remove the target user from the current user's 'following' list
    current_user.following.remove(target_user)
    return Response({"detail": f"Successfully unfollowed {target_user.username}."}, status=status.HTTP_200_OK)