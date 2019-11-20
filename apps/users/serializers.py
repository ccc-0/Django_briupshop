from rest_framework import serializers, validators
from .models import *

class AddressSerializer(serializers.ModelSerializer):
    user =serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ShopAddress
        fields = '__all__'
        # 验证器：三个联合唯一
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShopAddress.objects.all(),
                fields=('name','tel','address'),
                message="我爱你，该地址已有，亲，请勿重复添加哦"
            )
        ]
