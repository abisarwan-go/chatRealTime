# your_app_name/management/commands/check_redis.py
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Test Redis connection for Django Channels'

    def handle(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        if channel_layer is None:
            self.stdout.write(self.style.ERROR('Channel layer is not configured'))
            return

        try:
            async_to_sync(channel_layer.send)('test_channel', {'type': 'test.message'})
            self.stdout.write(self.style.SUCCESS('Redis connection is working'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Redis connection failed: {e}'))
