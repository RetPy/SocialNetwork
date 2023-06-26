from rest_framework import serializers

from apps.posts.models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        post = Post.objects.get(id=self.context['request'].parser_context['kwargs']['pk'])
        like = Like(
            user=self.context['request'].user,
            post=post
        )
        like.save()
        return like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'text',
            'created_at',
            'comments',
            'total_likes',
        )

    def create(self, validated_data):
        post = Post(**validated_data)
        post.user = self.context['request'].user
        post.save()
        return post

    @staticmethod
    def get_total_likes(obj):
        return obj.post_liked.count()
