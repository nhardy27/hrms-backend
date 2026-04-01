from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from api.Chat.model import ChatMessage
from api.UserProfile.model import UserProfile


class EmployeeListView(APIView):
    """
    GET /chat/employees/
    Returns list of all employees (excluding current user) for starting a chat.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.select_related('user', 'department', 'designation') \
            .exclude(user=request.user)
        data = []
        for p in profiles:
            data.append({
                'user_id': p.user.id,
                'username': p.user.username,
                'name': f"{p.first_name or ''} {p.last_name or ''}".strip() or p.user.username,
                'emp_code': p.emp_code,
                'department': p.department.name if p.department else None,
                'designation': p.designation.name if p.designation else None,
            })
        return Response(data)


class ChatHistoryView(APIView):
    """
    GET /chat/history/?room_type=private&room_id=1_2
    Returns paginated chat history for a room.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        room_type = request.query_params.get('room_type')
        room_id = request.query_params.get('room_id')

        if not room_type or not room_id:
            return Response({'error': 'room_type and room_id are required'}, status=400)

        messages = list(
            ChatMessage.objects.filter(
                room_type=room_type, room_id=room_id
            ).select_related('sender').order_by('created_at')[:100]
        )

        sender_ids = [m.sender_id for m in messages]
        profiles = {p.user_id: p for p in UserProfile.objects.filter(user_id__in=sender_ids)}

        data = []
        for m in messages:
            profile = profiles.get(m.sender_id)
            name = f"{profile.first_name or ''} {profile.last_name or ''}".strip() or m.sender.username if profile else m.sender.username
            data.append({
                'sender_id': m.sender.id,
                'sender': name,
                'message': m.message,
                'timestamp': m.created_at.isoformat(),
            })
        return Response(data)
