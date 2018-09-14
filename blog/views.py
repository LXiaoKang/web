from django.shortcuts import  get_object_or_404, render
from .models import Blog, BlogType

# 导入统计函数
from django.db.models import Count
# 导入分页的库
from django.core.paginator import Paginator
from datetime import datetime

# 导入 read_recoder应用的模型  这是自己定义的
from read_recoder.utils import read_recoder_read

from django.contrib.contenttypes.models import ContentType
# 导入 评论的 类
from comment.models import  Comment  
#   导入form表单提交评论
from comment.forms import CommentForm

# 将共同的 部分拿出来, 主要是分页
def get_blog_list_common_data(request,blogs_list_all):
    # 每10页进行分页
    #   paginator 分页器的实例化
    paginator = Paginator(blogs_list_all, 6)
    page_num = request.GET.get('page', 1) # 获取GET请求的内容，默认为1  获取url的页面参数(GET请求)
    page_of_blogs = paginator.get_page(page_num) # 将获取的第几页的文章列表值给赋值,get方法会自动处理异常
    current_page_num = page_of_blogs.number      #  获取当前页码

    # 页面范围  显示 分页时的 结果， 就是如果有多个分页，不完全显示，就显示4个页面
    #   获取当前页码和 当前页码的前后两页
    page_range = list(range( max(current_page_num-2, 1), current_page_num )) + \
                 list(range(current_page_num,  min(current_page_num+2, paginator.num_pages) + 1))

    #   加上省略页码
    if page_range[0] - 1 >= 2:
       page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 统计同类的文章的数量
    BlogType.objects.annotate(blog_count=Count('blog'))

    #   统计按照日期分类的数量       获取按照时间分类的对象
    # 字典用于存放,时间 和按照时间分类的文章数量
    blog_date_dict = {}  
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    for blog_date in blog_dates:
        blog_date_count = Blog.objects.filter(created_time__year=blog_date.year,
                                              created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_date_count
    context = {}
    # 获取当所有的文章列表 ,两行都是
    # context['blogs'] = Blog.objects.all()
    context['blogs'] = page_of_blogs.object_list
    # 获取当前页的文章列表 ,两行都是
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    #   获取文章分类列表随笔，djang，感悟，这行内容  本来是第一行,然后加了个统计数量 所以是下面的, blog是Blog类的小写
    # context['blog_types'] =  BlogType.objects.all()
    context['blog_types'] =  BlogType.objects.annotate(blog_count=Count('blog'))
    # 按照时间分类   添加 统计数量
    # context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    context['blog_dates'] = blog_date_dict
    return context

#   显示博客列表
def blog_list(request):

    blogs_list_all = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_list_all)
    return render(request,'blog/blog_list.html', context)


#   显示分类的内容
def blogs_with_type(request, blog_type_pk):


    # context ['type'] = get_object_or_404(BlogType, pk=blog_type_pk)
    #   获取文章的所属类型，
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    #   筛选   django有那些文章
    blogs_type_list_all = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_type_list_all)
    #   随笔
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html', context)

#   按照时间分类
def blogs_with_date(request, year, month):

    #   筛选   
    blogs_type_list_all = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_type_list_all)
    context['blogs_with_date'] = '%s年%s日' % (year, month)
    return render(request,'blog/blogs_with_type.html', context)

#   显示博客内容
def blog_detail(request, blog_pk):

    # 提交页面请求,
    blog = get_object_or_404(Blog, pk=blog_pk)  #   注意这里的类型,不是字符串, 获取id为blog_pk的文章

    # 调用 自己封装的 计数器
    read_cookie_key = read_recoder_read(request, blog)
    
    #  获取博客的 类型, 为了显示评论用的
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = {}
    context['comments'] = comments

    # 获取当前文章的 上一篇文章,按照时间排序,__表示大于   返回结果是一个 querySet,可能会有多个,所以加上last
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    #   获取下一篇  不用first也可以用[0]
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog 

    #   将表单 提交评论的 类实例化 并传给前台
    context['comment_form'] = CommentForm(initial={
        'content_type':blog_content_type.model, 'object_id':blog_pk
                                                  })
    # response = render(request,'blog/blog_detail.html', context)  #  响应 , 最好用下面的一句
    response = render(request, 'blog/blog_detail.html', context) 


    # true表示已经存在过, 后面两个选一个表示cookie的失效期, expirse=datetime , manx_age=60    
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie的标记
    return response

