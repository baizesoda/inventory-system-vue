from rest_framework import serializers
from .models import InOutRecord, StockCheck


class InOutRecordSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True, default='')

    class Meta:
        model = InOutRecord
        fields = '__all__'
        read_only_fields = ['operator']


class ScanInboundSerializer(serializers.Serializer):
    barcode = serializers.CharField()


class StockCheckSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = StockCheck
        fields = '__all__'
        read_only_fields = ['operator', 'recorded_stock', 'difference']
