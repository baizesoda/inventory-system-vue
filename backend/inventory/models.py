from django.db import models
from django.conf import settings


class InOutRecord(models.Model):
    TYPE_CHOICES = [('in', '入库'), ('out', '出库')]

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    type = models.CharField('类型', max_length=3, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField('数量')
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2, default=0)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='操作人')
    remark = models.CharField('备注', max_length=200, blank=True)
    created_at = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        db_table = 'in_out_record'
        ordering = ['-created_at']
        verbose_name = '出入库记录'


class StockCheck(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    recorded_stock = models.IntegerField('系统库存')
    actual_stock = models.IntegerField('实际库存')
    difference = models.IntegerField('差异', default=0)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='盘点人')
    created_at = models.DateTimeField('盘点时间', auto_now_add=True)

    class Meta:
        db_table = 'stock_check'
        verbose_name = '盘点记录'

    def save(self, **kwargs):
        self.difference = self.actual_stock - self.recorded_stock
        super().save(**kwargs)
