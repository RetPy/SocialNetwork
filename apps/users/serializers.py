from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.models import UserFollowing

User = get_user_model()


class BaseUserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = (
            'id',
            'user',
            'following',
        )
        read_only_fields = (
            'user',
            'following',
        )


class UserFollowingSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = (
            'user_id',
        )

    @staticmethod
    def get_user_id(obj):
        return obj.following.id


class UserFollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = (
            'user_id',
        )

    @staticmethod
    def get_user_id(obj):
        return obj.user.id


class UserSerializer(serializers.ModelSerializer):
    following = UserFollowingSerializer(many=True, read_only=True)
    followers = UserFollowerSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nickname',
            'about',
            'avatar',
            'following',
            'followers',
            'password',
            'confirm_password',
        )
        write_only_fields = (
            'password',
            'confirm_password',
        )

    def create(self, validated_data):
        if not validated_data['password'] or not validated_data['confirm_password']:
            raise serializers.ValidationError('Password is required!')
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError('Confirm password must be same with password!')
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
