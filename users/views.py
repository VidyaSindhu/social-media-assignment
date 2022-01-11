from datetime import date
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import User, UserFollower
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions, status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import string
from rest_framework_jwt.views import verify_jwt_token
from rest_framework.views import APIView

from .serializers import FollowUserSerializer, GetUserDetailSerializer, UserDetailSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class JSONWebTokenAuthentication(JSONWebTokenAuthentication):
    JSONWebTokenAuthentication.keyword = "Bearer"


class GetUsersList(ListAPIView):
    APIView = ['GET']
    permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class FollowUserView(CreateAPIView, DestroyAPIView):
    APIView = ['POST', 'DELETE']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserFollower.objects.all()
    serializer_class = FollowUserSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        follows_id = kwargs.get('id')
        if user_id != follows_id:
            request.data['user'] = user_id
            request.data['follows'] = follows_id
            return super().post(request, *args, **kwargs)
        else:
            return Response(
                data={
                    "message": "You cannot follow youself",
                    "success": False
                },
                status=406
            )

    def destroy(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            follows_id = kwargs.get('id')
            if user_id != follows_id:
                object = UserFollower.objects.get(
                    user=user_id, follows=follows_id)
        except UserFollower.DoesNotExist:
            return Response(
                data={
                    "message": "You donot follow the specified user",
                    "success": False
                },
                status=406
            )
        instance = object
        self.perform_destroy(instance)
        return Response(
            data={
                "success": True
            },
            status=status.HTTP_204_NO_CONTENT
        )


class UnfollowUserView(CreateAPIView):
    APIView = ['POST', 'DELETE']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserFollower.objects.all()
    serializer_class = FollowUserSerializer

    def post(self, request, *args, **kwargs):
        unfollow_id = kwargs.pop('id')
        user_id = request.user.id
        try:
            object = UserFollower.objects.get(follows=unfollow_id, user=user_id)
        except UserFollower.DoesNotExist:
            return Response(
                data={
                    "message": "You donot follow the specified user",
                    "success": False
                },
                status=406
            )
        else:
            object.delete()
        return Response(
            data={
                "success":True
            },
            status=status.HTTP_204_NO_CONTENT
        )

class GetUserDetailView(RetrieveAPIView):
    APIView = ['GET']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User.objects.all()
    serializer_class = GetUserDetailSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        folllowings = UserFollower.objects.filter(user=request.user.id).count()
        followers = UserFollower.objects.filter(follows=request.user.id).count()
        response_data = serializer.data
        response_data["followers"] = followers
        response_data['followings'] = folllowings
        return Response(response_data)



