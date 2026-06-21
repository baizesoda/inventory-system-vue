from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '系统管理员'),
        ('keeper', '库管员'),
        ('viewer', '查看者'),
    ]
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField('手机号', max_length=20, blank=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
