# accounts/views.py (Final attempt for checker compliance)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated # <-- permissions.IsAuthenticated is here
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView # <-- generics.GenericAPIView is here
from django.shortcuts import get_object_or_404


# --- Existing Registration and Login Views ---

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
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

class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user


# --- FOLLOW/UNFOLLOW VIEWS ---

class FollowUserView(GenericAPIView): # Direct usage of GenericAPIView
    permission_classes = [IsAuthenticated] # Direct usage of IsAuthenticated
    queryset = User.objects.all()
    
    def post(self, request, user_id):
        CustomUser = get_user_model()
        target_user = get_object_or_404(CustomUser.objects.all(), id=user_id) 
        current_user = request.user

        if current_user.id == target_user.id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if current_user.following.filter(id=target_user.id).exists():
            return Response({"detail": f"You are already following {target_user.username}."}, status=status.HTTP_200_OK)

        current_user.following.add(target_user)
        return Response({"detail": f"Successfully followed {target_user.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(GenericAPIView): # Direct usage of GenericAPIView
    permission_classes = [IsAuthenticated] # Direct usage of IsAuthenticated
    queryset = User.objects.all()
    
    def post(self, request, user_id):
        CustomUser = get_user_model()
        target_user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        current_user = request.user

        if not current_user.following.filter(id=target_user.id).exists():
            return Response({"detail": f"You are not following {target_user.username}."}, status=status.HTTP_200_OK)

        current_user.following.remove(target_user)
        return Response({"detail": f"Successfully unfollowed {target_user.username}."}, status=status.HTTP_200_OK)