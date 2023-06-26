from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics, response, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.core.cache import cache

from apps.users.models import UserFollowing
from apps.users.serializers import UserSerializer, BaseUserFollowingSerializer, UserFollowingSerializer
from utils.permissions import IsCurrentUser

User = get_user_model()


def get_user(user_id):
    user = cache.get(f'user:{user_id}', None)
    if user is None:
        user = User.objects.get(pk=user_id)
        cache.set(f'user:{user.id}', user, timeout=None)
    return user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        match self.action:
            case 'update' | 'delete':
                permission_classes = [IsAdminUser | IsCurrentUser]
            case 'list' | 'retrieve':
                permission_classes = [IsAuthenticated]
            case 'create':
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        user = get_user(kwargs.get("pk"))
        return response.Response(self.serializer_class(user).data)

    def perform_destroy(self, instance):
        cache.delete(f'user:{instance.id}')
        instance.delete()

    def perform_update(self, serializer):
        user = self.get_object()
        cache.set(f'user:{user.id}', user, timeout=None)
        serializer.save()


class UserFollowView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowingSerializer

    def post(self, request, *args, **kwargs):
        following_user = get_user(self.kwargs.get('pk'))
        following = UserFollowing.objects.get_or_create(user=request.user, following=following_user)
        return response.Response(BaseUserFollowingSerializer(following[0]).data)

    def delete(self, request, *args, **kwargs):
        following_user = get_user(self.kwargs.get('pk'))
        UserFollowing.objects.get(user=request.user, following=following_user).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        following_user = get_user(self.kwargs.get('pk'))
        try:
            following = UserFollowing.objects.get(user=request.user, following=following_user)
            return response.Response(BaseUserFollowingSerializer(following).data)
        except ObjectDoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
