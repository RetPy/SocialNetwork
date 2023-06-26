from django.contrib.admin import register, ModelAdmin

from apps.posts.models import Post, Comment, Like


@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('user', 'created_at',)


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_display_links = ('id', 'post')
    list_filter = ('post', 'user', 'created_at',)


@register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'created_at',)
