from django.db import models

# Create your models here.

#商品分类信息表
class GoodsType(models.Model):
    name = models.CharField(max_length=20,verbose_name='分类名称')
    level = models.IntegerField(verbose_name="分类级别")
    uper_type = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="上级编号",null=True,blank=True,related_name='son')

    class Meta():
        verbose_name = '商品分类信息表'

    def __str__(self):
        return self.name

#商品信息表
class Goods(models.Model):
    # good_id = models.IntegerField(primary_key=True, auto_created=True, verbose_name="商品id")
    name = models.CharField(max_length=20,verbose_name="商品名称")
    original_price = models.FloatField(verbose_name="原价")
    actual_price = models.FloatField(verbose_name="现价")
    freight = models.FloatField(verbose_name="运费")
    image = models.ImageField(verbose_name="商品主图",upload_to='uploads/goods/%Y/%m/%d')
    detail = models.CharField(verbose_name="说明",max_length=255)
    sale_nums = models.IntegerField(verbose_name="销量")
    all_nums = models.IntegerField(verbose_name="库存")
    view_nums = models.IntegerField(verbose_name="浏览量")
    favor_nums = models.IntegerField(verbose_name="收藏量")
    comment_nums = models.IntegerField(verbose_name="评论量")
    created_times = models.DateTimeField(verbose_name="录入时间")
    one_typename = models.ForeignKey('GoodsType',on_delete=models.CASCADE,related_name='one',null=True,blank=True,
                                     verbose_name="一级分类")
    two_typename = models.ForeignKey('GoodsType', on_delete=models.CASCADE,related_name='two',null=True,blank=True,
                                     verbose_name="二级分类")
    three_typename = models.ForeignKey('GoodsType', on_delete=models.CASCADE,related_name='three',null=True,blank=True,
                                       verbose_name="三级分类")

    class Meta():
        verbose_name= "商品信息表"

    def __str__(self):
        return self.name

class GoodsDisplayFiles(models.Model):
    goods = models.ForeignKey('Goods',on_delete=models.CASCADE,related_name='img')
    text = models.CharField(max_length=255,verbose_name="说明")
    goods_files = models.FileField(upload_to="uploads/goods/%Y/%m/%d",verbose_name="展示图")

    class Meta():
        verbose_name = '商品展示文件信息表'

    def __str__(self):
        return self.text
