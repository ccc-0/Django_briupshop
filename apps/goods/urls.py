from django.conf.urls import url
from django.urls import path

from .views import *

app_name = '[goods]'

urlpatterns = [
    url(r'^list/', GoodsListView.as_view(), name='goodlist'),
    path(r'typelist/',GoodsTypeView.as_view(),name='typelist') #商品分类列表

]