from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Blog, Post, SubscriptionsList


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ("pk", "username", "email")


class BlogSerializer(serializers.ModelSerializer):
    """
    Blog serializer
    """
    class Meta:
        model = Blog


class PostSerializer(serializers.ModelSerializer):
    """
    Post model serializer
    """
    read = serializers.SerializerMethodField()
    blog = BlogSerializer(read_only=True)

    def get_read(self, obj):
        """
        If user in post.users_read return true
        :param obj: Post objects
        :return: bool
        """
        return obj.users_read.filter(pk=self.context['request'].user.pk).exists()

    def create(self, validated_data):
        """
        Create post
        :param validated_data: dict
        :return: Post
        """
        post = Post()
        post.title = validated_data.pop('title')
        post.content = validated_data.pop('content')
        post.blog = self.context['request'].user.blog
        post.save()
        return post

    class Meta:
        model = Post
        exclude = ('users_read', )


class SubscriptionsListSerializer(serializers.ModelSerializer):
    """
    Subscription serializer
    """
    class Meta:
        model = SubscriptionsList

