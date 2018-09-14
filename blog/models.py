from django.db import models
from django.contrib.auth.models import User
# 添加富文本编辑器的库
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# 反向泛型关系, 添加7天内的热门博客,使用的
from django.contrib.contenttypes.fields import GenericRelation

from read_recoder.models import ReadNumExpandMethod, ReadDetail

# Create your models here.


#   博客分类
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    #   这里是返回显示的内容
    def __str__(self):
        return self.type_name

#   博文
class  Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    #   将BlogType和Blog关联起来
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)

    # 访问七天的阅读, 的热门博客
    read_details = GenericRelation(ReadDetail)
    
    # 阅读计数器 初始化
    read_num = models.IntegerField(default=0)
    
    content = RichTextUploadingField(config_name='default3')
    # content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)   
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)


    

    #   这里是返回显示的内容
    def __str__(self):
        return "<Blog:%s>" % self.title 

# 创建时间按照降序排序
    class Meta:
        ordering = ['-created_time']