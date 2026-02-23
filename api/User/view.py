from django.contrib.auth.models import User
from api.User.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from api.permissions import CustomPermission
from datetime import datetime

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        user = self.request.user

        # agar superuser hai → sab users dikhao
        if user.is_superuser:
            return User.objects.all()

        # warna sirf logged-in user ka data
        return User.objects.filter(id=user.id)

    @action(detail=True, methods=['post'])
    def send_offer_letter(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        # Format dates to dd/mm/yyyy
        offer_date = data.get('offer_date', '')
        joining_date = data.get('joining_date', '')
        
        if offer_date:
            try:
                offer_date = datetime.strptime(offer_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass
        
        if joining_date:
            try:
                joining_date = datetime.strptime(joining_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass
        
        context = {
            'candidate_name': f"{user.first_name} {user.last_name}",
            'candidate_email': user.email,
            'candidate_contact': data.get('candidate_contact', ''),
            'designation': data.get('designation', ''),
            'department': data.get('department', ''),
            'joining_date': joining_date,
            'basic_salary': data.get('basic_salary', ''),
            'hra': data.get('hra', ''),
            'allowance': data.get('allowance', ''),
            'offer_date': offer_date,
        }

        try:
            html_content = render_to_string('emails/offer_letter.html', context)
            email = EmailMultiAlternatives(
                subject="Offer Letter",
                body="Please find your offer letter attached.",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Offer letter sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to send email", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
