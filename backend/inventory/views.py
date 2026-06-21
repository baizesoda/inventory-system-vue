from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from products.models import Product
from .models import InOutRecord, StockCheck
from .serializers import InOutRecordSerializer, ScanInboundSerializer, StockCheckSerializer


class InOutRecordViewSet(viewsets.ModelViewSet):
    queryset = InOutRecord.objects.select_related('product', 'operator')
    serializer_class = InOutRecordSerializer
    filterset_fields = ['type', 'product']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        record = serializer.save(operator=self.request.user)
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=record.product_id)
            if record.type == 'in':
                product.stock += record.quantity
            else:
                product.stock -= record.quantity
            product.save(update_fields=['stock'])


@api_view(['POST'])
def scan_inbound(request):
    ser = ScanInboundSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    barcode = ser.validated_data['barcode']

    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(barcode=barcode)
            product.stock += 1
            product.save(update_fields=['stock'])
            InOutRecord.objects.create(
                product=product, type='in', quantity=1,
                unit_price=product.cost, operator=request.user, remark='扫码入库',
            )
    except Product.DoesNotExist:
        return Response({'error': '未找到该条码对应的商品'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'product': product.name, 'stock': product.stock})


class StockCheckViewSet(viewsets.ModelViewSet):
    queryset = StockCheck.objects.select_related('product', 'operator')
    serializer_class = StockCheckSerializer

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.request.data['product'])
        serializer.save(operator=self.request.user, recorded_stock=product.stock)
