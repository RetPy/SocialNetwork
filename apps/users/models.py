from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(
        max_length=30,
    )
    about = models.TextField(
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='user_avatars',
        default='default_avatar.jpg',
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.username)


class UserFollowing(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    followed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user', 'following')

    def __str__(self):
        return f'{self.user} follow {self.following}'
