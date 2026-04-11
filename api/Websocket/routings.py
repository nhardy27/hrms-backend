from django.urls import path
from api.Websocket.consumers import PrivateChatConsumer, DepartmentChatConsumer, DesignationChatConsumer, NotificationConsumer

# WebSocket URL patterns — works like urls.py but for ws:// connections.
websocket_urlpatterns = [
    path('ws/chat/private/<str:room_id>/', PrivateChatConsumer.as_asgi()),       # 1-to-1 private chat
    path('ws/chat/department/<str:room_id>/', DepartmentChatConsumer.as_asgi()), # Department group chat
    path('ws/chat/designation/<str:room_id>/', DesignationChatConsumer.as_asgi()), # Designation group chat
    path('ws/notifications/', NotificationConsumer.as_asgi()),                   # Per-user push notifications
]
