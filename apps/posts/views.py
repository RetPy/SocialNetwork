from rest_framework import viewsets, generics

from apps.posts.models import Post, Like, Comment
from apps.posts.serializers import PostSerializer, LikeSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



