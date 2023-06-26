from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_post'
    )
    title = models.CharField(
        max_length=255,
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_liked',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_liked',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user} to {self.post}'


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comment'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comment'
    )
    text = models.TextField(
        max_length=550,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='parent_comment',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.user}: {self.text}'
