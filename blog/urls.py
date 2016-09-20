from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^blogs$', views.BlogListAPIView.as_view(), name='blogs'),
    url(r'^blog/(?P<pk>\d+)/$', views.PostListAPIView.as_view(), name='blog'),
    url(r'^posts$', views.UserPostListAPIView.as_view(), name='posts'),
    url(r'^post/(?P<pk>\d+)/$', views.PostAPIView.as_view(), name='post'),
    url(r'^post/create$', views.PostCreateAPIView.as_view(), name='post_create'),
    url(r'^post/read/(?P<pk>\d+)/$', views.SetPostReadAPIView.as_view(), name='post_read'),
    url(r'^subscribe/(?P<pk>\d+)/$', views.AddDelSubscrptionAPIView.as_view(), name='subscribe')
]