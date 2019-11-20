from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[operations]'

urlpatterns = [
    path(r'favorlist/',FavorListView.as_view(),name='favorlist'), #收藏夹
    path(r'favorcreate/', FavorCreateView.as_view(), name='favorcreate'),  # 加入收藏夹
    path(r'favordelete/<int:pk>', FavorDeleteView.as_view(), name='favordelete'),  # 取消收藏
    path(r'favordetail/<int:pk>', FavorDetailView.as_view(), name='favordetail'),  # 获取单条数据详情
    path(r'favorupdate/<int:pk>', FavorUpdateView.as_view(), name='favorupdate'),  #修改收藏夹

    path(r'addresscreate/',CartCreateView.as_view(), name='addresscreate'),  #增
    path(r'addressdelete/<int:pk>',CartDeleteView.as_view(), name='addressdelete'),#删
    path(r'addressupdate/<int:pk>',CartUpdateView.as_view(), name='addressupdate'),#改
    path(r'addresslist/',CartListView.as_view(), name='addresslist'),#查

]