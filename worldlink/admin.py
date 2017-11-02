from django.contrib import admin
from .models import Profile
from .models import Post, Like, Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
