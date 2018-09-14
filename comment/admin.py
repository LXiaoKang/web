from django.contrib import admin
from .models import Comment

# Register your models here.
#   注册
@admin.register(Comment)
#   后台显示自定义类
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_type','text', 'comment_time', 'comment_people')