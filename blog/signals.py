from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .tasks import send_email_task


@receiver(post_save, sender=Post, dispatch_uid='created_post')
def created_post(sender, instance, created, *args, **kwargs):
    print("Trooloolo")
    if created:
        subscrbers = instance.blog.subscribers.all()
        if subscrbers.exists():
            email_list = [subscriber.user.email for subscriber in subscrbers]
            email_message = "Hello! New post added<a href={url}>{post}</a> ".format(url=instance.get_absolute_url(),
                                                                                post=instance.title)
            send_email_task.delay("Post added", email_message, "admin@test.ru", email_list)


# post_save.connect(created_post, sender=Post)
