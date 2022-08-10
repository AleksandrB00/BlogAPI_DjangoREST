import email
from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag
from django.contrib.auth.models import User


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tag = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    
    class Meta:
        model = Post
        fields = ('id', 'h1', 'text', 'author', 'post_date', 'image', 'slug', 'tag')
        lookup_field = 'slug'
        extra_kwargs = {
            'url' : {'lookup_field' : 'slug'}
        }

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)
        lookup_field = 'name'
        extra_kwargs = {
            'url' : {'lookup_field' : 'name'}
        }

class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()

class SignUpSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({
                'password' : 'Пароли не совпадают'
            })
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileEditSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        confirm_password = validated_data['confirm_password']
        if  instance.password != confirm_password:
            raise serializers.ValidationError({
                'password' : 'Пароли не совпадают'
            })
        instance.save()
        return instance

class PostCreateSerializer(serializers.ModelSerializer):

    tag = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'h1', 'text', 'author', 'post_date','image', 'slug', 'tag']

    