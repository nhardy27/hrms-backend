from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(user_id, title, message, data=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notification_{user_id}',
        {
            'type': 'send_notification',
            'title': title,
            'message': message,
            'data': data or {},
        }
    )
