from django.shortcuts import render, redirect

from .models import Comment
# 导入的这个库 用处很多, 用来找到 文章的类
from django.contrib.contenttypes.models import ContentType

# 重定向redirect, 反向解析 reverse
from django.urls import reverse

# Create your views here.
# 对提交的评论信息进行处理
def update_comment(request):
    # 因为返回的时候 还需要返回到原来的页面, 所以要用到重定向,  reverser表示如果 第一个找到不到, 重定向到第二个
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    user = request.user

    print(type(referer))
    print(referer)

    # 数据检查
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录', 'redirect_to' : referer})

    # 提交的内容, 对应的博客id, 博客类型, 如果没有的话就返回空格
    text = request.POST.get('text', ' ').strip()   # strip是去掉空格的意思
    # 如果评论内容为空
    if text=='':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to' : referer})

    try:
        # 因为id是 整数, 而从前端提交的是字符型,所以强制转换
        object_id = int(request.POST.get('object_id', ' '))
        content_type = request.POST.get('content_type', ' ') 
        # 为了做的通用, 所以这里用 这种方法 来查找 评论的文章所属类型,
        #  先找到 该评论所属的类型,是博客,还是其他内容, 再找到 具体的文章在数据库中的id 
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj   = model_class.objects.get(pk=object_id) 
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to' : redirect(referer)})

    # 检查通过, 保存评论
    # 对评论的类实例化
    comment = Comment()
    comment.text = text
    # 这里出现个错误, 就是因为,这里的user和数据库的user不一样, 一个是user一个是comment_people
    comment.comment_people = user
    # comment.user = user   
    comment.content_object = model_obj
    comment.save()  

    return redirect(referer)