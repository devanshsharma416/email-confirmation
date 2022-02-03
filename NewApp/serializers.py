from dataclasses import fields
import email
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name')

class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

        extra_kwargs = {
                    'email': {'required': True},
                    'first_name': {'required': True},
                    'last_name': {'required': True},
                    "password": {"write_only": True}
         }
    
    def validate(self, attrs):
        email = attrs['email']

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"User already Exists"})
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def create(self, validate_data):
        user = User.objects.create_user(validate_data['first_name'], validate_data['last_name'], validate_data['email'])
        user.set_password(validate_data['password'])
        return user
