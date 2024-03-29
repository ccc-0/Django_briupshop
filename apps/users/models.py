from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#收获地址
class ShopAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name="收货人姓名")
    tel = models.CharField(max_length=20,verbose_name="联系方式")
    address = models.CharField(max_length=255,verbose_name="收获地址")
    zipcode = models.IntegerField(verbose_name="邮编")
    is_default = models.BooleanField(verbose_name="是否默认",default=False)

    class Meta():
        verbose_name = "收获地址"

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    STATUS = (
        (1,'男'),
        (2,'女'),
        (3,'保密')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    gender = models.IntegerField(choices=STATUS, verbose_name='用户性别')
    userphoto = models.ImageField(upload_to='uploads/user/%Y/',verbose_name='用户头像')
