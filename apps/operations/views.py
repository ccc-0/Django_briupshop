from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import mixins
from users.views import IsOwnerOrReadOnly
from .models import *
from .serializers import FavorSerializer,Cartserializer

# Create your views here.

#收藏夹列表
class FavorListView(generics.ListAPIView):
    '''收藏夹列表'''
    queryset = Favor.objects.all()
    # queryset = Favor.objects.filter(user = request.user) 错误做法
    serializer_class = FavorSerializer
    #过滤返回当前用户的收藏夹
    def get_queryset(self):
        # queryset = Favor.objects.filter(user=self.request.user)
        # return queryset
        return super().get_queryset().filter(user=self.request.user)  #调用父类，父类必须存在

#加入收藏夹  新增
class FavorCreateView(generics.CreateAPIView):
    '''新增收藏'''
    serializer_class = FavorSerializer

    #自定义返回结果
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try: #失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code':400,'message':'收藏失败'},status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #成功后返回信息的定制
        res = Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        res.data['code']=200
        res.data['message']= "亲，收藏成功了哦"
        return res

#删除收藏   删除-delete
class FavorDeleteView1(generics.DestroyAPIView):
    '''删除收藏'''
    queryset =  Favor.objects.all()
    serializer_class = FavorSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    #重新destroy方法，自定义返回结果
    def destroy(self, request, *args, **kwargs):
        #自定义失败返回信息
        try:
            instance = self.get_object()
        except:
            return Response(data={'code':400,'message':'亲，取消收藏失败，请重新操作哦'},status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(data={'code': 200, 'message': "亲，您已取消收藏"}, status=status.HTTP_204_NO_CONTENT)
        #错误  Respons中没有data不能后面res=...
        # res = Response(status=status.HTTP_204_NO_CONTENT)
        # res.data['code']=200
        # res.data['message']='亲，您已取消收藏'
        # return res

#删除收藏   删除-get
class FavorDeleteView(generics.GenericAPIView):
    queryset =  Favor.objects.all()
    serializer_class = FavorSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self,request,pk):
        #获取地址url中的参数
        # favor_id = self.kwargs.get('pk','')
        try:
            #自定义视图手动调用check_object_permissions验证对象级权限
            obj = Favor.objects.get(pk=pk)   #使用get获取单条数据
            self.check_object_permissions(request, obj)

            obj.delete()
        except:
            return Response(data={'code': 400, 'message': '亲，删除失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'亲，删除成功'},status=status.HTTP_200_OK)

#这条不符合收藏夹逻辑，只是知识点介绍
#获取单条数据详情
class FavorDetailView(generics.RetrieveAPIView):
    queryset = Favor.objects.all()
    serializer_class = FavorSerializer

class FavorUpdateView1(generics.UpdateAPIView):
    queryset = Favor.objects.all()
    serializer_class = FavorSerializer
    #put  ：单体整该（单条数据整体修改）
    #patch:局部修改（一条数据中的某些列的值）

class FavorUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''修改收藏'''
    queryset = Favor.objects.all()
    serializer_class = FavorSerializer
    #数据编辑用post方式
    def post(self,request,*args,**kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request,*args,**kwargs)  #调用UpdateModelMixin方法
        except:
            return Response(data={'code':400,'message':'修改失败',},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)




class CartCreateView(generics.CreateAPIView):
    '''新增购物车'''
    serializer_class = Cartserializer

class CartDeleteView(generics.DestroyAPIView):
    '''删除购物车'''
    queryset = ShoppingCart.objects.all()
    serializer_class = Cartserializer

class CartUpdateView(generics.UpdateAPIView):
    '''修改购物车'''
    queryset = ShoppingCart.objects.all()
    serializer_class = Cartserializer

class CartListView(generics.ListAPIView):
    '''购物车列表'''
    queryset = ShoppingCart.objects.all()
    serializer_class = Cartserializer
