from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from utilitities.otp import OTP_EXPIRATION_TIME


from authentication.models import CustomUser
from django.utils import timezone

from utilitities.email import EmailSender
from utilitities.otp import get_otp
from ashpotexamine.config.django.base import DEBUG
from utilitities.logging import LoggingMixin


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: Request):
    user_id = request.data.get('user_id')
    password = request.data.get('password')

    try:
        # Fetch the user by user_id
        user = CustomUser.objects.get(user_id=user_id)
  
        # Verify the password
        if user.check_password(password):
        
            if user.is_superuser: #check if is_super user

                otp = get_otp() # call the get_otp() function to get the opt
                
                if DEBUG:
                    try:
                        otp_email = EmailSender(subject='Login OTP')
                        # call the send_otp_email method to actually do the email sending
                        otp_email.send_otp_email(email=user.email, first_name=user.first_name, otp_code=otp,time = OTP_EXPIRATION_TIME)
                        return Response({"message": f"OTP sent to {user.email}",'role':'superuser',"redirect_page": 'verify-otp.html',"message_type":"success"}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({"message": f"Error sending OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    LoggingMixin(message=f"Your OTP is :{otp}. It will expire in {OTP_EXPIRATION_TIME}").log()
                
            elif user.is_staff:
                pass

            elif user.is_student and user.is_active:
                user.last_login = timezone.now()
                return Response(data={"message":"success",'role':'student',"redirect_page":"students-dashboard.html"})    
        return Response({"message": "Either ID Number or Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
       
        return Response({"message": "Either ID Number or Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
