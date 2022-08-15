from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagView.as_view()),
    path('tags/<slug:tag_slug>/', TagDetailView.as_view()),
    path('aside/', AsideView.as_view()),
    path('feedback/', FeedBackView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('profile_view/', ProfileView.as_view()),
    path('profile_edit/', ProfileEditView.as_view()),
    path('create_post/', PostCreateView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<slug:post_slug>/', CommentView.as_view()),
]