from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from .models import User, UserFollower
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password



class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name')

class GetUserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)

class FollowUserSerializer(ModelSerializer):

    class Meta:
        model = UserFollower
        fields = ('user', 'follows')