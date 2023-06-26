from rest_framework import serializers

from apps.posts.models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    post_liked = LikeSerializer(many=True, read_only=True)
    # total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'text',
            'created_at',
            'comments',
            'post_liked',
            # 'total_likes'
        )

    def create(self, validated_data):
        post = Post(**validated_data)
        post.user = self.context['request'].user
        return post

    def get_total_likes(self):
        return len(self.validated_data['post_liked'])
