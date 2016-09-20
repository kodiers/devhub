from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status

from .models import Blog, SubscriptionsList, Post
from .serializers import BlogSerializer, PostSerializer, SubscriptionsListSerializer, UserSerializer

# Create your views here.


class BlogListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


class PostListAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(data={"error": "blog not found"}, status=status.HTTP_404_NOT_FOUND)
        posts = blog.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPostListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        blogs = self.request.user.subscription.subscriptions.all()
        posts = Post.objects.filter(blog__in=blogs).order_by('-created')
        return posts


class PostAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class SetPostReadAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # http_method_names = ['PUT', 'DELETE']

    def put(self, request, *args, **kwargs):
        context = {'request': request}
        post = self.get_object()
        post.users_read.add(request.user)
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        context = {'request': request}
        post = self.get_object()
        post.users_read.remove(request.user)
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)


class AddDelSubscrptionAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    http_method_names = ['PUT', 'DELETE']

    def put(self, request, *args, **kwargs):
        blog = self.get_object()
        request.user.subscription.subscriptions.add(blog)
        return Response(data={'status': 'subscribed'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        request.user.subscription.subscriptions.remove(blog)
        return Response(data={'status': 'unsubscribed'}, status=status.HTTP_200_OK)
