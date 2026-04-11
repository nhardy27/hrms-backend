import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


def get_room_name(room_type, room_id):
    # Generates a unique channel group name like: chat_private_1_2
    return f"chat_{room_type}_{room_id}"


@database_sync_to_async
def get_user_and_display_name(token_key):
    # Validates JWT token and returns (User, display_name). Returns (None, None) on failure.
    from api.UserProfile.model import UserProfile
    try:
        token = AccessToken(token_key)
        user = User.objects.get(id=token['user_id'])
        try:
            profile = UserProfile.objects.get(user=user)
            display_name = f"{profile.first_name or ''} {profile.last_name or ''}".strip() or user.username
        except UserProfile.DoesNotExist:
            display_name = user.username
        return user, display_name
    except Exception:
        return None, None


@database_sync_to_async
def get_room_participants(room_type, room_id):
    # Returns distinct sender IDs who have messaged in this room (used for group notifications).
    from api.Chat.model import ChatMessage
    return list(
        ChatMessage.objects.filter(room_type=room_type, room_id=str(room_id))
        .values_list('sender_id', flat=True).distinct()
    )


@database_sync_to_async
def save_message(sender, room_type, room_id, message):
    # Persists a chat message to the database and returns the created instance.
    from api.Chat.model import ChatMessage
    return ChatMessage.objects.create(
        sender=sender,
        room_type=room_type,
        room_id=str(room_id),
        message=message
    )


@database_sync_to_async
def get_chat_history(room_type, room_id):
    # Fetches last 50 messages for a room, enriched with sender display names.
    from api.Chat.model import ChatMessage
    from api.UserProfile.model import UserProfile
    messages = list(
        ChatMessage.objects.filter(
            room_type=room_type,
            room_id=str(room_id)
        ).select_related('sender').order_by('created_at')[:50]
    )

    sender_ids = [m.sender_id for m in messages]
    profiles = {p.user_id: p for p in UserProfile.objects.filter(user_id__in=sender_ids)}

    result = []
    for m in messages:
        profile = profiles.get(m.sender_id)
        if profile:
            display_name = f"{profile.first_name or ''} {profile.last_name or ''}".strip() or m.sender.username
        else:
            display_name = m.sender.username
        result.append({
            'sender_id': m.sender.id,
            'sender': display_name,
            'message': m.message,
            'timestamp': m.created_at.isoformat()
        })
    return result


def extract_token(query_string):
    # Extracts the JWT token from the WebSocket query string (?token=<jwt>).
    params = parse_qs(query_string.decode())
    tokens = params.get('token', [])
    return tokens[0] if tokens else None


class BaseChatConsumer(AsyncWebsocketConsumer):
    """
    Base consumer for group-style chat rooms (department, designation).
    Subclasses set `room_type` to define the room category.
    """
    room_type = None

    async def connect(self):
        token = extract_token(self.scope['query_string'])
        self.user, self.display_name = await get_user_and_display_name(token)

        if not self.user:
            await self.accept()
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid or expired token.'}))
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = get_room_name(self.room_type, self.room_id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send chat history to the newly connected client.
        history = await get_chat_history(self.room_type, self.room_id)
        await self.send(text_data=json.dumps({'type': 'history', 'messages': history}))

    async def disconnect(self, close_code):
        # Remove this channel from the room group on disconnect.
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, ValueError):
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid JSON.'}))
            return

        message = data.get('message', '').strip()
        if not message:
            return

        saved = await save_message(self.user, self.room_type, self.room_id, message)

        # Broadcast the message to all users in the room group.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_id': self.user.id,
                'sender': self.display_name,
                'message': message,
                'timestamp': saved.created_at.isoformat(),
            }
        )

        # Push notification to participants who are not the sender.
        await self._notify_participants(message)

    async def _notify_participants(self, message):
        # Sends a push notification to all room participants except the sender.
        participant_ids = await get_room_participants(self.room_type, self.room_id)
        for uid in participant_ids:
            if uid != self.user.id:
                await self.channel_layer.group_send(
                    f'notification_{uid}',
                    {
                        'type': 'send_notification',
                        'title': self.display_name,
                        'message': message,
                        'data': {
                            'room_type': self.room_type,
                            'room_id': self.room_id,
                            'sender_id': self.user.id,
                        },
                    }
                )

    async def chat_message(self, event):
        # Handler called by group_send; forwards the message to the WebSocket client.
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender_id': event['sender_id'],
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }))


class PrivateChatConsumer(BaseChatConsumer):
    """
    Handles 1-to-1 private chat.
    Room ID is derived from sorted user IDs to ensure both sides share the same room.
    """
    room_type = 'private'

    async def connect(self):
        token = extract_token(self.scope['query_string'])
        self.user, self.display_name = await get_user_and_display_name(token)

        if not self.user:
            await self.accept()
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid or expired token.'}))
            await self.close()
            return

        self.receiver_id = int(self.scope['url_route']['kwargs']['room_id'])
        # Sort IDs so both users always resolve to the same room name.
        ids = sorted([str(self.user.id), str(self.receiver_id)])
        self.room_id = f"{ids[0]}_{ids[1]}"
        self.room_group_name = get_room_name(self.room_type, self.room_id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        history = await get_chat_history(self.room_type, self.room_id)
        await self.send(text_data=json.dumps({'type': 'history', 'messages': history}))

    async def _notify_participants(self, message):
        # For private chat, only the receiver gets a notification.
        await self.channel_layer.group_send(
            f'notification_{self.receiver_id}',
            {
                'type': 'send_notification',
                'title': self.display_name,
                'message': message,
                'data': {
                    'room_type': self.room_type,
                    'room_id': self.room_id,
                    'sender_id': self.user.id,
                },
            }
        )


class DepartmentChatConsumer(BaseChatConsumer):
    # Group chat scoped to a department room.
    room_type = 'department'


class DesignationChatConsumer(BaseChatConsumer):
    # Group chat scoped to a designation room.
    room_type = 'designation'


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Dedicated consumer for real-time push notifications.
    Each user joins their own group: notification_<user_id>.
    """
    async def connect(self):
        token = extract_token(self.scope['query_string'])
        self.user, _ = await get_user_and_display_name(token)

        if not self.user:
            await self.accept()
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid or expired token.'}))
            await self.close()
            return

        # Each user has a personal notification group keyed by their user ID.
        self.group_name = f'notification_{self.user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the personal notification group on disconnect.
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        # Forwards an incoming notification event to the WebSocket client.
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event.get('title', ''),
            'message': event.get('message', ''),
            'data': event.get('data', {}),
        }))
