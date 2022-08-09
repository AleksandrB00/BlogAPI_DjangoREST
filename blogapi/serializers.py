from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    
    class Meta:
        model = Post
        fields = ('id', 'h1', 'text', 'author', 'post_date', 'image', 'slug', 'tag')
        lookup_field = 'slug'
        extra_kwargs = {
            'url' : {'lookup_field' : 'slug'}
        }