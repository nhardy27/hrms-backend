from django.urls import path
from api.Websocket.consumers import PrivateChatConsumer, DepartmentChatConsumer, DesignationChatConsumer

websocket_urlpatterns = [
    path('ws/chat/private/<str:room_id>/', PrivateChatConsumer.as_asgi()),
    path('ws/chat/department/<str:room_id>/', DepartmentChatConsumer.as_asgi()),
    path('ws/chat/designation/<str:room_id>/', DesignationChatConsumer.as_asgi()),
]
