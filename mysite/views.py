from  django.shortcuts import render, redirect, reverse

# 将 自定义的方法导入进来
from read_recoder.utils import get_seven_days_read_data, get_today_hot_datas, \
                               get_yeserday_hot_datas
#   添加 django自带的计数 库
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
#   数据库的聚合函数,的求和方法
from django.db.models import Sum

# 获取时间, python中的库
import datetime
from django.utils import timezone

# 导入缓存的库的方法, 访问缓存
from django.core.cache import cache

#   如何登录用户
from django.contrib.auth import authenticate, login

from .form import LoginForm, RegForm

# 重定向redirect, 反向解析 reverse
from django.urls import reverse

#  注册的
from django.contrib.auth.models import User



# 对七天的热门博客 进行统计
def get_7_day_hot_blogs():
    today = timezone.now().date()
    dates = today-datetime.timedelta(days=7)
    # 根据id 和 title 进行分组,对 阅读数 进行统计求和
    blogs = Blog.objects \
                        .filter(read_details__date__lt=today, read_details__date__gte=dates) \
                        .values('id', 'title') \
                        .annotate(read_num_sum = Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    
    return blogs[:7]


# def get_yeserday_hot_datas():
#     yeserday = timezone.now().date() - datetime.timedelta(days=1)

#     read_details = Blog.objects.filter(read_details__date=yeserday).values('id', 'title').order_by('-read_num')

#     return read_details[:7]

def home(request):
    
    blog_content_type = ContentType.objects.get_for_model(Blog)

    # 返回的是blog, 获取七天的阅读数据
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    #   获取当天的阅读的热门,文章, 这里的返回的 是一个 query set
    today_hot_datas = get_today_hot_datas(blog_content_type)


    hot_blogs_for_days_key = cache.get('hot_blogs_for_days_key') 
    if hot_blogs_for_days_key is None:
        hot_blogs_for_days_value = get_7_day_hot_blogs()
        cache.set('hot_blogs_for_days_key', hot_blogs_for_days_value, 1)
        print('no_use_cache')
    else:
        print('use_cache')

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_datas'] = today_hot_datas

    # print("****************")
    # print(today_hot_datas)
                                    #   获取昨天的阅读的热门,文章, 这里的返回的 是一个 query set
    context['yeserday_hot_datas'] = get_yeserday_hot_datas(blog_content_type)
    # context['yeserday_hot_datas'] = get_yeserday_hot_datas()

    context['hot_blogs_for_days'] = get_7_day_hot_blogs()
    # context['hot_blogs_for_days'] = hot_blogs_for_days_key
    return render(request,'home.html', context)

# 登录按钮的 功能, 就是登录
def login_m(request):
    # 对于 post提交的数据 接收,, 这里的get方法也可以, 用哪一个都行
    '''
    if  :为了折叠
        username = request.POST['username']
        password = request.POST.get('password')

        # 这句 是对后天的数据进行验证匹配, user是返回结果
        user = authenticate(request, username=username, password=password)

        # 获取 请求头, 就是从哪个链接进来的,  获取不到就返回首页, 也可以重定向,reverse('home')
        referer = request.META.get('HTTP_REFERER', '/')

        if user is not None:
            login(request, user)
            # 重定向, 进来的页面
            return  redirect(referer)
        else:
            return render(request, 'error.html', {'message': '用户名或密码不正确'})

    '''
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    if request.method == 'POST':
        # 实例化
        login_form = LoginForm(request.POST)
        # 检查数据
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            # 重定向, from是 前端传来的 
            # return redirect(request.GET.get('from'))
            return redirect(request.GET.get('from', reverse('home')))

            # return redirect(referer)
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


#   注册 功能  
def register(request):
    # 如果是post方法,就用post方法实例化, 不是就用一般的方法实例化
    if request.method == 'POST':
        regform = RegForm(request.POST)
        #   检查数据
        if regform.is_valid():
            username = regform.cleaned_data['username']
            email    = regform.cleaned_data['email']
            password = regform.cleaned_data['password']
            #   创建用户, 实例化一个 user对象,并保存
            user = User.objects.create_user(username, email, password)
            user.save()
            #   或者
            
            # user = User()
            # user.username=username
            # user.email=email
            # user.set_password=password
            # user.save()
            
            # 登录用户
                    # 与后台进行,验证
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        regform = RegForm()

    context = {}
    context['regform'] = regform
    return render(request, 'regform.html', context)



