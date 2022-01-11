from django.http import request, response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from posts.serializers import AllPostDetailsSerializer, CommentOnPostSerializer, LikedPostSerializer, PostDetailsSerializer, PostSerializer
from .models import Post, PostLikedBy, CommentOnPost
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions, status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db.models import Case, Count, When, IntegerField, Sum, Q

# Create your views here.

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class JSONWebTokenAuthentication(JSONWebTokenAuthentication):
    JSONWebTokenAuthentication.keyword = "Bearer"


class PostView(RetrieveAPIView, CreateAPIView, DestroyAPIView):
    APIView = ['GET', 'POST', 'DELETE']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data.pop('created_by')
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        self.queryset = Post.objects.annotate(likes=Count('liked_post', filter=Q(
            liked_post__liked=True))).filter(created_by=request.user.id)
        self.serializer_class = PostDetailsSerializer
        return super().get(request, *args, **kwargs)


class LikePostView(CreateAPIView):
    APIView = ['POST']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = PostLikedBy.objects.all()
    serializer_class = LikedPostSerializer

    def post(self, request, *args, **kwargs):
        liked_by = request.user
        post = kwargs.get('id')
        request.data['post'] = post
        request.data['liked_by'] = liked_by
        try:
            object, created = PostLikedBy.objects.update_or_create(
                post=post, liked_by=liked_by, defaults={'liked': True})
        except Exception as e:
            return Response(
                data={
                    "success": False,
                    "message": e.args
                },
                status=400
            )
        else:
            return Response(
                data={
                    "success": True
                },
                status=status.HTTP_201_CREATED
            )


class UnlikePostView(CreateAPIView):
    APIView = ['POST']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = PostLikedBy.objects.all()
    serializer_class = LikedPostSerializer

    def post(self, request, *args, **kwargs):
        liked_by = request.user
        post = kwargs.get('id')
        request.data['post'] = post
        request.data['liked_by'] = liked_by
        try:
            object, created = PostLikedBy.objects.update_or_create(
                post=post, liked_by=liked_by, defaults={'liked': False})
        except Exception as e:
            return Response(
                data={
                    "success": False,
                    "message": e.args
                },
                status=400
            )
        else:
            return Response(
                data={
                    "success": True
                },
                status=status.HTTP_201_CREATED
            )


class CommentOnPostView(CreateAPIView):
    APIView = ['POST']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = CommentOnPost.objects.all()
    serializer_class = CommentOnPostSerializer

    def post(self, request, *args, **kwargs):
        commented_by = request.user
        post = kwargs.pop('id')
        post_instance = Post.objects.get(pk=post)
        comment = CommentOnPost.objects.create(
            post=post_instance, comment=request.data['comment'], commented_by=commented_by)
        return Response(
            data={
                "id": comment.id
            },
            status=status.HTTP_201_CREATED
        )


class GetAllPostDetailsView(ListAPIView):
    APIView = ['GET']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Post.objects.annotate(likes=Count(
        'liked_post', filter=Q(liked_post__liked=True))).order_by('-created_at')
    serializer_class = AllPostDetailsSerializer

    def get_queryset(self):
        return Post.objects.annotate(likes=Count(
        'liked_post', filter=Q(liked_post__liked=True))).filter(created_by=self.request.user.id).order_by('-created_at')