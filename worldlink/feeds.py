from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestEntriesFeed(Feed):
    title = "Top news"
    link = "/sitenews/"
    description = "Updates on changes and additions to posts."

    def items(self):
        return Post.objects.order_by('-created_date')[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('post_detail', args=[item.pk])
