
# 获取时间, python中的库
import datetime
#   添加 django自带的计数 库
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail

from django.utils import timezone

#   数据库的聚合函数,的求和方法
from django.db.models import Sum
# 这里封装了 一些 写好的方法, 方便到时候调用

# 计数器增加的方法
def read_recoder_read(request, obj):

    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    # 当不存在 这个键值时 在加1
    # if not request.COOKIES.get(key):
    #     ct = ContentType.objects.get_for_model(obj)
    #
    #     '''
    if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        # 存在记录
        readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
    else:
        #   不存在对应的记录
        readnum = ReadNum(content_type=ct, object_id=obj.pk)
    '''
    # 修改上面的为这一句, get_or_create 如果有 就加, 没有就创建, 返回为一个元祖,或者是创建
    #   总阅读数加1
    readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    readnum.read_num += 1


    readnum.save()


    #   统计当天加的数量
    date = timezone.now().date()
    '''


    readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    readnum.read_num += 1


    readnum.save()

    #   统计当天加的数量
    date = timezone.now().date()

    if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #   存在当天的记录
        readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
    else:
        #   不存在当天的记录
        readDetail = ReadDetail(content_type=ct, object_id=obj.pk)

    readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
    readDetail.read_num += 1
    readDetail.save()
    return key


# 获取七天的阅读数据
def get_seven_days_read_data(content_type):
    # 获取当天时间
    today = timezone.now().date()
    # 用于保存每天的阅读量的和
    read_nums_everyday = []

    dates = []

    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        # 将时间以字符串的格式保存
        dates.append(date.strftime('%y/%m/%d'))
        # 得到的是 当天的 阅读次数, 因为有多条 所以利用数据库的聚合函数,sum
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # print(ReadDetail.objects.all())
        # 利用数据库,的求和 统计每天的 访问总数, 返回值是一个字典
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        # 将数据 放在一个字典中, 如果为空 就返回0
        read_nums_everyday.append(result['read_num_sum'] or 0)

    return dates, read_nums_everyday

# 当天 获取热门 博客, 并且直选前7篇
def get_today_hot_datas(content_type):
    today = timezone.now().date()   
    # 返回的结果是Query set              # 对查询结果进行排序, 由大到小
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
   
    return read_details[:7]

# 获取昨天热门 博客, 并且直选前7篇
def get_yeserday_hot_datas(content_type):
    yeserday = timezone.now().date() - datetime.timedelta(days=1)

    read_details = ReadDetail.objects.filter(content_type=content_type, date=yeserday).order_by('-read_num')

    return read_details[:7]


