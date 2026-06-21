from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('records', views.InOutRecordViewSet)
router.register('checks', views.StockCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scan/inbound/', views.scan_inbound),
]
