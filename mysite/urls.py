"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

#   上传图片的url 导入，
#   导入配置文件settings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    #   首页
    path('', views.home, name='home'),
    #   管理页面
    path('admin/', admin.site.urls),
    #   blog 文章内容总页面
    path('blog/', include('blog.urls')),

    #   库规定好的  在pypi-python中找django-ckeditor， url
    path('ckeditor', include('ckeditor_uploader.urls')),

    #   用户登录页面的跳转页面
    path('login_m/', views.login_m, name='login_m'),
    #   用户注册 功能
    path('register/', views.register, name='register'),

    #  处理评论的
    path('comment/', include('comment.urls')),
]

#   上传图片添加访问链接
#   前一个参数 是
#   开发中用，在部署时不用这个
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

