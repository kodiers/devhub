from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Blog, Post, SubscriptionsList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "email")


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog


class PostSerializer(serializers.ModelSerializer):
    read = serializers.SerializerMethodField()

    def get_read(self, obj):
        if self.context['request'].user.is_authenticated():
            if self.context['request'].user in obj.users_read.all():
                return True
        return False

    def create(self, validated_data):
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
    class Meta:
        model = SubscriptionsList

