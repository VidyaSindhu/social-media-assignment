"""social_media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken

from users.views import FollowUserView, GetUserDetailView, GetUsersList
from posts.views import CommentOnPostView, GetAllPostDetailsView, LikePostView, PostView, UnlikePostView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authenticate/', ObtainJSONWebToken.as_view()), #POST
    path('api/verify/', VerifyJSONWebToken.as_view()), #POST
    path('api/users/all', GetUsersList.as_view()), #GET
    path('api/follow/<int:id>/', FollowUserView.as_view()), #POST
    path('api/unfollow/<int:id>/', FollowUserView.as_view()), #POST
    path('api/user', GetUserDetailView.as_view()), #GET

    #POST app
    path('api/posts/', PostView.as_view()), #POST
    path('api/posts/<int:pk>/', PostView.as_view()), #DELETE
    path('api/like/<int:id>/', LikePostView.as_view()), #POST
    path('api/unlike/<int:id>/', UnlikePostView.as_view()), #DELETE
    path('api/comment/<int:id>/', CommentOnPostView.as_view()), #POST
    path('api/all_posts/', GetAllPostDetailsView.as_view()), #POST
    
]
