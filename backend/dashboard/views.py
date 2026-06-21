from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
from inventory.models import InOutRecord


@api_view(['GET'])
def overview(request):
    today = timezone.now().date() if timezone.is_aware(timezone.now()) else timezone.now().replace(hour=0, minute=0, second=0).date()
    products = Product.objects.filter(is_active=True)

    total_products = products.count()
    total_value = sum(p.stock * p.cost for p in products)
    today_in = InOutRecord.objects.filter(type='in', created_at__date=today).aggregate(s=Sum('quantity'))['s'] or 0
    today_out = InOutRecord.objects.filter(type='out', created_at__date=today).aggregate(s=Sum('quantity'))['s'] or 0

    low_stock = list(
        products.filter(stock__lt=F('safety_stock'))
        .values('id', 'name', 'stock', 'safety_stock')[:10]
    )

    categories = list(
        Category.objects.annotate(
            product_count=Count('product', filter=Q(product__is_active=True)),
            total_stock=Sum('product__stock', filter=Q(product__is_active=True)),
        ).values('name', 'product_count', 'total_stock')
    )

    return Response({
        'total_products': total_products,
        'total_value': float(total_value),
        'today_in': today_in,
        'today_out': today_out,
        'low_stock': low_stock,
        'categories': categories,
    })


@api_view(['GET'])
def trend(request):
    today = timezone.now().date() if timezone.is_aware(timezone.now()) else timezone.now().replace(hour=0, minute=0, second=0).date()
    days = int(request.query_params.get('days', 30))
    start = today - timedelta(days=days - 1)

    records = InOutRecord.objects.filter(created_at__date__gte=start)
    data = []
    for i in range(days):
        d = start + timedelta(days=i)
        day_records = records.filter(created_at__date=d)
        data.append({
            'date': d.isoformat(),
            'in': day_records.filter(type='in').aggregate(s=Sum('quantity'))['s'] or 0,
            'out': day_records.filter(type='out').aggregate(s=Sum('quantity'))['s'] or 0,
        })

    return Response(data)
