from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse


# django hosts --> subdomain for reverse


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    content = models.TextField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def owner(self):
        return self.user.username

    # def get_absolute_url(self):
        # return reverse("api_posting:post_rud", kwargs={'pk': self.pk}) '/api/posting/1/'

    def get_api_url(self, request=None):
         return reverse("api_posting:post_rud ", kwargs={'pk': self.pk})