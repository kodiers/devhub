import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status

from .models import Blog, Post
from .serializers import BlogSerializer, PostSerializer

# Create your views here.


class BlogListAPIView(generics.ListAPIView):
    """
    Get all blogs
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


class PostListAPIView(APIView):
    """
    Get all posts in blog
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        """
        :param request: HttpRequest
        :param pk: int Blog.pk
        :return: HttpResponse (json)
        """
        context = {'request': request}
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(data={"error": "blog not found"}, status=status.HTTP_404_NOT_FOUND)
        posts = blog.posts.all()
        serializer = PostSerializer(posts, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPostListAPIView(generics.ListAPIView):
    """
    Get post in user subscription list
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        blogs = self.request.user.subscription.subscriptions.all()
        posts = Post.objects.filter(blog__in=blogs).order_by('-created')
        return posts


class PostAPIView(generics.RetrieveAPIView):
    """
    Get one post
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    """
    Create post
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class SetPostReadAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Add/remove user to post.users_read
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        context = {'request': request}
        post = self.get_object()
        if 'read' in request.session:
            read_values = json.loads(request.session['read'])
        else:
            read_values = list()
        read_values.append(post.pk)
        request.session['read'] = json.dumps(read_values)
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        context = {'request': request}
        post = self.get_object()
        if 'read' in request.session:
            del request.session['read']
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)


class AddDelSubscrptionAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Add/remove blog to user subscription list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def put(self, request, *args, **kwargs):
        blog = self.get_object()
        request.user.subscription.subscriptions.add(blog)
        return Response(data={'status': 'subscribed'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        request.user.subscription.subscriptions.remove(blog)
        return Response(data={'status': 'unsubscribed'}, status=status.HTTP_200_OK)
