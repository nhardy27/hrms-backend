import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


def get_room_name(room_type, room_id):
    return f"chat_{room_type}_{room_id}"


@database_sync_to_async
def get_user_and_display_name(token_key):
    """Fetch user + display name in a single DB call."""
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
def save_message(sender, room_type, room_id, message):
    from api.Chat.model import ChatMessage
    return ChatMessage.objects.create(
        sender=sender,
        room_type=room_type,
        room_id=str(room_id),
        message=message
    )


@database_sync_to_async
def get_chat_history(room_type, room_id):
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
    params = parse_qs(query_string.decode())
    tokens = params.get('token', [])
    return tokens[0] if tokens else None


class BaseChatConsumer(AsyncWebsocketConsumer):
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

        history = await get_chat_history(self.room_type, self.room_id)
        await self.send(text_data=json.dumps({'type': 'history', 'messages': history}))

    async def disconnect(self, close_code):
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

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender_id': event['sender_id'],
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }))


class PrivateChatConsumer(BaseChatConsumer):
    room_type = 'private'

    async def connect(self):
        token = extract_token(self.scope['query_string'])
        self.user, self.display_name = await get_user_and_display_name(token)

        if not self.user:
            await self.accept()
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid or expired token.'}))
            await self.close()
            return

        receiver_id = self.scope['url_route']['kwargs']['room_id']
        ids = sorted([str(self.user.id), str(receiver_id)])
        self.room_id = f"{ids[0]}_{ids[1]}"
        self.room_group_name = get_room_name(self.room_type, self.room_id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        history = await get_chat_history(self.room_type, self.room_id)
        await self.send(text_data=json.dumps({'type': 'history', 'messages': history}))


class DepartmentChatConsumer(BaseChatConsumer):
    room_type = 'department'


class DesignationChatConsumer(BaseChatConsumer):
    room_type = 'designation'
