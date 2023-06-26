from django.contrib.admin import register, ModelAdmin
from django.contrib.auth import get_user_model

from apps.users.models import UserFollowing

User = get_user_model()


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'date_joined',)
    list_display_links = ('id', 'username', 'nickname',)
    search_fields = ('id', 'username', 'nickname')


@register(UserFollowing)
class UserFollowingAdmin(ModelAdmin):
    list_display = ('id', 'user', 'following')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'following')
