from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=50, unique=True)
    code = models.CharField('分类编码', max_length=20, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = '商品分类'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('商品名称', max_length=100)
    sku = models.CharField('SKU', max_length=50, unique=True)
    barcode = models.CharField('条形码', max_length=64, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类')
    specification = models.CharField('规格', max_length=100, blank=True)
    price = models.DecimalField('售价', max_digits=10, decimal_places=2, default=0)
    cost = models.DecimalField('成本', max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField('库存数量', default=0)
    safety_stock = models.IntegerField('安全库存', default=10)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'product'
        verbose_name = '商品'

    def __str__(self):
        return f'{self.name} ({self.sku})'

    @property
    def is_low_stock(self):
        return self.stock < self.safety_stock
