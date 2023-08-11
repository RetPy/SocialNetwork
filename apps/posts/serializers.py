from rest_framework import serializers

from apps.posts.models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('request'):
            self.fields['parent'].queryset = Comment.objects.filter(post=self.get_current_post())

    def get_current_post(self):
        return Post.objects.get(id=self.context['request'].parser_context['kwargs']['pk'])

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['post'] = self.get_current_post()
        comment = Comment(**validated_data)
        comment.save()
        return comment


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
