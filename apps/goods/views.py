from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse
from .serializers import *
from .schemas import *
from .filters import GoodsFilter
from rest_framework import generics
import json

# Create your views here.

class GoodsListView1(View):
    def  get(self,request):
        #逻辑处理
        # goodslist = Goods.objects.all()
        # goods=[] #构建存放所有商品字典的列表
        # for good in goodslist:
        #     goodsdict={} #将商品信息注意存放在字典中
        #     goodsdict['name']=good.name
        #     goodsdict['actual_price']=good.actual_price
        #     goods.append(goodslist)
        # goodslist_json = json.dumps(goodslist)

        goodslist = Goods.objects.values()
        goodslist = list(goodslist) #将Queryset 转化为列表
        for good in goodslist: #图片和创建时间特殊
            good['image'] = str(good['image'])
            good['create_time'] = str(good['create_time'])
        goodslist_json = json.dumps(goodslist)

        return HttpResponse(goodslist_json)
        # return render(request,'')

class GoodsListView2(View):
    def get(self, request):

        goodslist = Goods.objects.values()
        goodslist = list(goodslist)  # 将Queryset 转化为列表
        for good in goodslist:  # 图片和创建时间特殊
            good['image'] = str(good['image'])
            good['created_time'] = str(good['created_time'])

        # goodslist_json = json.dumps(goodslist)
        # return HttpResponse(goodslist_json)
        # JsonResponse自动打包
        return JsonResponse(goodslist,safe=False)

class GoodsListView3(APIView):
    '''
    商品列表页
    '''
    def get(self, request):
        goodslist = Goods.objects.all()
        #采用序列化器  多条数据需写many=True
        serializers_json = GoodsListSerialzer(goodslist,many=True)

        return Response(serializers_json.data)

#使用mixins
from rest_framework import mixins
class GoodsListView4(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = Goods.objects.all()
    serializer_class = GoodsListSerialzer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#分页
class GoodsPagination(PageNumberPagination):
    page_size = 1  #每页显示条数
    page_size_query_param = 'page_size'
    max_page_size = 100 #每页最大条数
    page_query_param = 'p' #分页参数变量名

class GoodsListView(generics.ListAPIView):
    '''
    商品列表+商品详情good_id
    '''
    queryset = Goods.objects.all() #查询结果集设置
    serializer_class = GoodsListSerialzer  #序列化器设置
    pagination_class = GoodsPagination  #不指定就采用默认自带的分页器，采用全局配置
    schema = GoodsListSchema   #指定所采用的schema，

    permission_classes = () #不要认证登录设置，   权限认证配置
    # permission_classes = (IsAuthenticated) #需要登录

    #过滤
    def get_queryset(self):
        # self.request.data(:Post/GET/FILES/PUT/PATCH) 获取任意一种形式的数据 以表单形式(schema_form)  self.request.data.get('id','')
        # self.request.query_params:GET  #传参  true:id=1&name='xx'  error:url:/detail/<int:id>/， (schema_query)

        # print(self.request.path)   #获取请求路径,url中配置的路径
        # print(self.kwargs)    #获取url中的参数字典形式

        good_id = self.request.query_params.get('good_id','')
        if good_id:
            queryset_filter = Goods.objects.filter(pk=good_id) #获取具体商品信息
        else:
            queryset_filter =Goods.objects.all()
        return queryset_filter


class GoodsListView6(generics.ListAPIView):
    '''
    商品列表+商品详情good_id
    '''
    queryset = Goods.objects.all() #查询结果集设置
    serializer_class = GoodsListSerialzer  #序列化器设置
    pagination_class = GoodsPagination  #不指定就采用默认自带的分页器，采用全局配置
    # schema = GoodsListSchema   #指定所采用的schema，
    #过滤器使用
    # (DjangoFilterBackend过滤,SearchFilter搜索,OrderingFilter排序）
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_fields =('name','detail')  #完全匹配   采用自定义过滤器后无效果
    search_fields =('name','detail')  #模糊查询- 搜索
    ordering_fields = ('actual_price','sale_nums')
    #使用自定义过滤器
    filterset_class = GoodsFilter

#商品分类信息列表
class GoodsTypeView(generics.ListAPIView):
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerialzer3
    schema = TypeListSchema  #配置schema
    pagination_class = None  #不需要分页时

    def get_queryset(self):
        # type_id = self.request.data.get('type_id','')
        type_id = self.request.query_params.get('type_id','')
        if type_id:
            queryset = GoodsType.objects.filter(id=type_id)
        else:
            queryset = GoodsType.objects.all()
        return queryset

