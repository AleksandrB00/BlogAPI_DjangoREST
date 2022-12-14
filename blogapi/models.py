from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User



class Post(models.Model):
    h1 = models.CharField(max_length=100)
    text = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateField(default=timezone.now)
    image = models.ImageField()
    slug = models.SlugField(max_length=100, unique=True)
    tag = TaggableManager()

    def __str__(self) -> str:
        return self.h1

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text