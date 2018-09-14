from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User


from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.

class Comment(models.Model):
    # 从文档中复制的   foreignKey是一对多 ,或多对一的关系, OneToOneField表示一对一
    # 这样就可以评论任何对应的字段
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论内容的字段
    # text = models.TextField()
    text = RichTextField(config_name='default3')
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_people = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    # user= models.ForeignKey(User, on_delete=models.DO_NOTHING)

# 创建时间按照降序排序
    class Meta:
        ordering = ['-comment_time']