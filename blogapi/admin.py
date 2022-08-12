from django.contrib import admin
from .models import Post, Comment


class AdminPanel(admin.ModelAdmin):
   pass

admin.site.register(Post, AdminPanel)
admin.site.register(Comment, AdminPanel)