from rest_framework import serializers, validators
from .models import *


class FavorSerializer(serializers.ModelSerializer):
    #隐藏user字段并且赋值为当前登录用户
    user= serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Favor
        fields = "__all__"
        extra_kwargs = { #对模型已有参数重新设置和编辑
            'created_time':{'required':False,'read_only':True}
        }
        #验证器：收藏夹用户和商品的联合唯一限制
        validators=[
            validators.UniqueTogetherValidator(
                queryset=Favor.objects.all(),
                fields = ('user','goods'),
                message="我爱你，该商品已收藏，亲，请勿重复收藏哦"
            )
        ]

class FavorSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Favor
        fields = '__all__'


class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
