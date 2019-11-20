from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status, mixins, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *

def jwt_response_payload_handler(token,user=None,request=None):
    #通过用户user对象即可获取用户相关的其他信息
    return {
        'token':token,
        'user':user.username,
        'test':'test',
    }

#自定义登录验证
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None

#对象级权限
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限，仅允许对象的所有者编辑它。
    假设模型实例具有 `owner` 属性。
    """
    print(123123)
    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许 GET，HEAD 或 OPTIONS 请求。
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # 实例必须具有名为 `owner` 的属性。
        return obj.user == request.user

# Create your views here.

class AddressCreateView(generics.CreateAPIView):
    #不用写queryset
    serializer_class = AddressSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '增加失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 成功后返回信息的定制
        res = Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        res.data['code'] = 200
        res.data['message'] = "亲，增加成功了哦"
        return res


class AddressDeleteView(generics.DestroyAPIView):
    queryset = ShopAddress.objects.all()
    serializer_class = AddressSerializer

    # 重新destroy方法，自定义返回结果
    def destroy(self, request, *args, **kwargs):
        # 自定义失败返回信息
        try:
            instance = self.get_object()
        except:
            return Response(data={'code': 400, 'message': '亲，取消收藏失败，请重新操作哦'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(data={'code': 200, 'message': "亲，您已取消收藏"}, status=status.HTTP_204_NO_CONTENT)


class AddressUpdateView1(generics.UpdateAPIView):
    queryset = ShopAddress.objects.all()
    serializer_class = AddressSerializer

class AddressUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    queryset = ShopAddress.objects.all()
    serializer_class = AddressSerializer
    #数据编辑用post方式
    def post(self,request,*args,**kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request,*args,**kwargs)  #调用UpdateModelMixin方法
        except:
            return Response(data={'code':400,'message':'修改失败',},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

class AddressListView(generics.ListAPIView):
    queryset = ShopAddress.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        # return ShopAddress.objects.filter(user=self.request.user)
        return super().get_queryset().filter(user=self.request.user)
