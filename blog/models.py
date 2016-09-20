from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

# Create your models here.


class Blog(models.Model):
    """
    Blog model
    """
    user = models.OneToOneField(User, verbose_name="User", related_name='blog')

    def __str__(self):
        return "Blog of {}".format(self.user.username)


class Post(models.Model):
    """
    Post model
    """
    blog = models.ForeignKey(Blog, related_name='posts', verbose_name="Blog")
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    users_read = models.ManyToManyField(User, related_name="read_posts", verbose_name="Users read", blank=True)

    def get_absolute_url(self):
        return reverse_lazy('blog:post', args=[self.pk])

    def __str__(self):
        return self.title


class SubscriptionsList(models.Model):
    """
    Subscription model
    """
    user = models.OneToOneField(User, verbose_name="User", related_name="subscription")
    subscriptions = models.ManyToManyField(Blog, related_name="subscribers", verbose_name="Subscriptions", blank=True)

    def __str__(self):
        return "{} subscription list".format(self.user.username)

