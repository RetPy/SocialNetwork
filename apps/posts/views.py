from rest_framework import viewsets, generics, permissions, response, status

from apps.posts.models import Post, Like, Comment
from apps.posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from utils.permissions import IsOwnerUser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.get_queryset()
    serializer_class = PostSerializer


class LikeAPIView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Like.objects.filter(post=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        Like.objects.get(post=self.kwargs['pk'], user=request.user).delete()
        return response.Response(status=status.HTTP_404_NOT_FOUND)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.request.parser_context['kwargs']['pk'])


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAdminUser | IsOwnerUser,)

    def get_queryset(self):
        return Comment.objects.get(id=self.request.parser_context['kwargs']['comm_pk'])
