from django.urls import path
from . import views

#   以blog开头, 这里是子路由
urlpatterns = [

    # http://localhost:8000/blog/1
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    #   博客分类 
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),

    #   博客列表
    # http://localhost:8000/blog/
    path('', views.blog_list, name='blog_list'),

    # 按照日期分类
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]