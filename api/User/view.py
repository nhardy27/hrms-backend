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
from api.Designation.model import Designation
from datetime import datetime

class UserViewset(ModelViewSet):
    """
    ViewSet for User management.
    Provides CRUD operations and custom actions like sending offer letters.
    """
    serializer_class = UserSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        """
        Filter queryset based on user role:
        - Superuser: can see all users
        - Normal user: can only see their own data
        """
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(id=user.id)

    @action(detail=True, methods=['post'])
    def send_offer_letter(self, request, pk=None):
        """
        Custom action to send offer letter email to a user.
        Endpoint: POST /api/v1/user/{id}/send_offer_letter/
        """
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
        
        # Resolve designation name from UUID if needed
        designation_val = data.get('designation', '')
        try:
            desig_obj = Designation.objects.get(id=designation_val)
            designation_val = desig_obj.name
        except (Designation.DoesNotExist, Exception):
            pass

        # Prepare email context
        basic_salary = int(data.get('basic_salary', 0) or 0)
        hra = int(data.get('hra', 0) or 0)
        allowance = int(data.get('allowance', 0) or 0)
        pf_deduction = round(basic_salary * 0.12)
        net_salary = basic_salary + hra + allowance - pf_deduction

        context = {
            'candidate_name': f"{user.first_name} {user.last_name}",
            'candidate_email': user.email,
            'candidate_contact': data.get('candidate_contact', ''),
            'designation': designation_val,
            'department': data.get('department', ''),
            'joining_date': joining_date,
            'basic_salary': basic_salary,
            'hra': hra,
            'allowance': allowance,
            'pf_deduction': pf_deduction,
            'net_salary': net_salary,
            'offer_date': offer_date,
        }

        try:
            # Render HTML template and send email
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
