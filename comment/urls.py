from django.urls import path
from . import views

urlpatterns = [
    # 处理评论的path
    path('update_comment', views.update_comment, name='update_comment')    
]


