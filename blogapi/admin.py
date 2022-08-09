from django.contrib import admin
from .models import Post


class AdminPanel(admin.ModelAdmin):
   pass

admin.site.register(Post, AdminPanel)