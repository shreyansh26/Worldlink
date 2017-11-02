from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.utils.translation import gettext as _

# Create your models here.
class Profile(models.Model):
    user = models.CharField(max_length=20)
    url = models.CharField(max_length=200, default='static "photos/profile-default.png"')
    image = models.ImageField(_("Profile Pic"), upload_to = 'worldlink/static/images', default = 'static/images/profile-default.png')
    image_url = models.CharField(max_length=50, default="photos/profile-default.png")
    name = models.CharField(max_length=50)
    date_of_birth =  models.DateField(_("Date of Birth"), default=datetime.date.today, null=True, blank=True)
    hobbies = models.TextField()
    education = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to = 'worldlink/static/images', default = '', blank=True, null=True)
    image_url = models.CharField(max_length=50, default="")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey('auth.User')
    post = models.ForeignKey(Post )
    #created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

