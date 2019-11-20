from rest_framework import serializers
from goods.models import Goods,GoodsType,GoodsDisplayFiles


#商品列表序列化
class GoodsListSerialzer1(serializers.Serializer):
    name = serializers.CharField(required=True)
    actual_price = serializers.IntegerField(required=True)

#商品类型序列化
class GoodsTypeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = GoodsType
        fields = '__all__'  # 获取全部列

class GoodsDisplaySerialzer(serializers.ModelSerializer):
    class Meta:
        model = GoodsDisplayFiles
        fields = '__all__'

#商品信息序列化器
class GoodsListSerialzer(serializers.ModelSerializer):
    one_typename = GoodsTypeSerialzer() #序列化拿外键的信息
    two_typename = GoodsTypeSerialzer()
    three_typename = GoodsTypeSerialzer()  #一找一  （外找主表）
    img = GoodsDisplaySerialzer(many=True) #related_name反向查找  一找多（主表找外表）
    class Meta:
        model = Goods
        # fields =('name','actual_price')
        # exclude = ('name',)  #不包含，反选，不能与fields同时出现
        fields = '__all__' #获取全部列


#商品分类信息
class GoodsTypeSerialzer1(serializers.ModelSerializer):
    class Meta:
        model = GoodsType
        fields = "__all__"

class GoodsTypeSerialzer2(serializers.ModelSerializer):
    son = GoodsTypeSerialzer1(many=True)
    class Meta:
        model = GoodsType
        fields = "__all__"

class GoodsTypeSerialzer3(serializers.ModelSerializer):
    son = GoodsTypeSerialzer2(many=True) #models外键设置属性related_name = son 一级分类
    class Meta:
        model = GoodsType
        fields = "__all__"