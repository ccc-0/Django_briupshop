from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[users]'

urlpatterns = [
    path(r'addresscreate/',AddressCreateView.as_view(), name='addresscreate'),  #增
    path(r'addressdelete/<int:pk>',AddressDeleteView.as_view(), name='addressdelete'),#删
    path(r'addressupdate/<int:pk>',AddressUpdateView.as_view(), name='addressupdate'),#改
    path(r'addresslist/',AddressListView.as_view(), name='addresslist'),#查

]