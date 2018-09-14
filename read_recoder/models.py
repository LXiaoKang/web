from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#   添加 django自带的计数 库
from django.contrib.contenttypes.models import ContentType
# 导入异常处理的库
from django.db.models.fields import exceptions

# 引用django的工具,中的timezone类, 添加当天的时间
from django.utils import timezone

# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    # 从文档中复制的   foreignKey是一对多 ,或多对一的关系, OneToOneField表示一对一
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 计数器的 拓展方法, 为了
class ReadNumExpandMethod():
    #   为了更通用性 把它定义到一个类里,然后让其他类去继承
    # 阅读计数
    def get_read_num(self):
        
        # 异常处理作为 没有找到阅读访问 就置为0
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist :
            return 0

#   阅读的模型
class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)

    read_num = models.IntegerField(default=0)

    # 从文档中复制的   foreignKey是一对多 ,或多对一的关系, OneToOneField表示一对一
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')