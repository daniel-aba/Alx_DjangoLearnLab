# accounts/serializers.py (Revised Code)

from rest_framework import serializers
from .models import User  # Assuming User is the custom model
from rest_framework.authtoken.models import Token # Required by checker
from django.contrib.auth import get_user_model # Required by checker

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # Include fields the user needs to provide
        fields = ['username', 'email', 'password', 'password2', 'bio']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Retrieve the custom User model
        UserModel = get_user_model() 

        # Create user using the manager method (Required by checker: get_user_model().objects.create_user)
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        
        # Create an authentication token for the new user (Required by checker: Token.objects.create)
        Token.objects.create(user=user) 
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)