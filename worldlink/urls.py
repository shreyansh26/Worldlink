from django.conf.urls import url

from . import views
from worldlink.feeds import LatestEntriesFeed

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^editprofile/$', views.edit_profile, name='edit_profile'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^newsfeed/$', views.post_list, name='post_list'),
    url(r'^newsfeed/post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^newsfeed/post/new/$', views.post_new, name='post_new'),
    url(r'^newsfeed/post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^search/$', views.search, name='search'),
    url(r'^viewprofile/(?P<user>[\w\d]+)/$', views.viewprofile, name='view_profile'),
    url(r'^follow/(?P<user_profile>[\d\w]+)/$', views.follow_user, name='follow_user'),
    url(r'^unfollow/(?P<user_profile>[\d\w]+)/$', views.unfollow_user, name='unfollow_user'),
    url(r'^like/(?P<pk>\d+)/$', views.like, name='like'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^memegenerator/$', views.meme_gen, name='meme_gen'),
    url(r'^ajax/save_image/$', views.save_image, name='save_image'),
    url(r'^notifications/$', views.Notifications, name='notifications'),
    url(r'^proflist/$$', views.ListProfileView.as_view(), name='profile-list', ),
    url(r'^latest/feed/$', LatestEntriesFeed(), name='latest-posts',),
    url(r'^ajax/like/$', views.update_like, name='update_like'),
]
#url(r'^video/(?P<userprofile>.+)/$'
