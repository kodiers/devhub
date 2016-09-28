import json
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Blog, Post, SubscriptionsList

# Create your tests here.


class BlogTestCase(TestCase):
    def setUp(self):
        usr1 = User.objects.create_user('user1', 'user1@mail.mm', 'p@ssw0rd')
        usr2 = User.objects.create_user('user2', 'user2@mail.mm', 'p@ssw0rd')
        self.blog1 = Blog.objects.create(user=usr1)
        self.blog2 = Blog.objects.create(user=usr2)
        self.post = Post.objects.create(blog=self.blog1, title='Test 1', content='Text')
        Post.objects.create(blog=self.blog2, title='Test 2', content='Text')
        SubscriptionsList.objects.create(user=usr1)
        SubscriptionsList.objects.create(user=usr2)

    def test_blogs(self):
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.get('/blog/blogs')
        self.assertEquals(response.status_code, 200)

    def test_blog(self):
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.get('/blog/blog/' + str(self.blog1.pk) + '/')
        self.assertContains(response, 'Test 1')

    def test_posts(self):
        self.client.login(username='user2', password='p@ssw0rd')
        self.client.put('/blog/subscribe/' + str(self.blog1.pk) + '/')
        response = self.client.get('/blog/posts')
        self.assertContains(response, 'Test 1')

    def test_post(self):
        self.client.login(username='user2', password='p@ssw0rd')
        response = self.client.get('/blog/post/' + str(self.post.pk) +'/')
        self.assertContains(response, 'Test 1')

    def test_create_post(self):
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.post('/blog/post/create', data={'title': 'test', 'content': 'test'})
        self.assertEquals(response.status_code, 201)

    def test_subscription(self):
        self.client.login(username='user2', password='p@ssw0rd')
        response = self.client.put('/blog/subscribe/' + str(self.blog1.pk) +'/')
        self.assertContains(response, 'subscribed')

    def test_as_read(self):
        self.client.login(username='user2', password='p@ssw0rd')
        response = self.client.put('/blog/post/read/' + str(self.post.pk) +'/')
        self.assertContains(response, 'true')
