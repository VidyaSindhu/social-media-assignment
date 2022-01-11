from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from .models import Post, PostLikedBy, CommentOnPost

class PostSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at', 'created_by')
        optional_fields = ['id', 'created_at']

class LikedPostSerializer(ModelSerializer):
    class Meta:
        model = PostLikedBy
        fields = ('post', 'liked_by')

class CommentOnPostSerializer(ModelSerializer):
    class Meta:
        model = CommentOnPost
        fields = ('id', 'post', 'comment', 'commented_by')
        optional_fields = ['id']

class PostDetailsSerializer(ModelSerializer):
    comments = serializers.StringRelatedField(many=True)
    likes = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'likes', 'comments')

class AllPostDetailsSerializer(ModelSerializer):
    comments = serializers.StringRelatedField(many=True)
    likes = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at', 'likes', 'comments')
