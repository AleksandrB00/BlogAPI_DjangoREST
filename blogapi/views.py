from rest_framework import viewsets, permissions, pagination, generics, filters
from .serializers import *
from .models import Post
from rest_framework.response import Response
from taggit.models import Tag
from rest_framework.views import APIView
from django.core.mail import send_mail



class PaginationView(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    ordering = 'post_date'

class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['text', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PaginationView

class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PaginationView
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tag=tag)

class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class AsideView(generics.ListAPIView):
    queryset = Post.objects.order_by('-id')[:3]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    def post(self, request):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['your_mail'])
            return Response({'success': 'Sent'})

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user' : UserSerializer(user, context=self.get_serializer_context()).data,
            'message' : 'Пользователь успешно создан',
        })

class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        return Response({
            'user_info': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })

class ProfileEditView(generics.GenericAPIView):
    serializer_class = ProfileEditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user' : UserSerializer(user, context=self.get_serializer_context()).data,
            'message' : 'Пользователь успешно изменён',
        })

class PostCreateView(generics.GenericAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            'post' : PostSerializer(post, context=self.get_serializer_context()).data,
            'message' : 'Пост успешно создан',
        })

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs['post_slug']
        post = Post.objects.get(slug=slug)
        return Comment.objects.filter(post=post)

class AddCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]