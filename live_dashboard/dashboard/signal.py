from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import StockSerializer
import json

@receiver(post_save, sender=Stock)
def send_stock_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        stocks = Stock.objects.all()
        stocks_data = StockSerializer(stocks, many=True).data
        async_to_sync(channel_layer.group_send)(
            'stock_updates',
            {
                'type': 'stock_update',
                'data': stocks_data,
            }
        )