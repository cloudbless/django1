from django.db import models
from django.utils import timezone
 
class Product(models.Model):
    # 产品类型选项更新为页面中的导航名称
    PRODUCTS_CHOICES = (
        ('robot', '牛客'),
        ('monitor', '学校oj'),
        ('face', 'vjudge'),
    )
    title = models.CharField(max_length=50, verbose_name='平台名称')  # 对应页面的{{productName}}
    description = models.TextField(verbose_name='平台详情')  # 对应页面的说明文字
    productType = models.CharField(choices=PRODUCTS_CHOICES,
                                   max_length=50,
                                   verbose_name='算法平台类型')  # 对应页面的"算法平台"分类
    price = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='推荐指数')
    publishDate = models.DateTimeField(default=timezone.now,  # 移除无效的max_length参数
                                       verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)
 
    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name = '算法平台'  # 对应页面的"算法平台"标题
        verbose_name_plural = '算法平台'
        ordering = ('-publishDate', )
class ProductImg(models.Model):
    product = models.ForeignKey(Product,
                                related_name='productImgs',
                                verbose_name='产品',
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Product/',
                              blank=True,
                              verbose_name='产品图片')
 
    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'