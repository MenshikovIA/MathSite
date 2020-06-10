from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:15]
