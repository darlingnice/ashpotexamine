from django.shortcuts import render,redirect

from utilitities.otp import OTP_EXPIRATION_TIME


from authentication.models import CustomUser
from django.utils import timezone

from utilitities.email import EmailSender
from utilitities.otp import get_otp
from ashpotexamine.config.django.base import DEBUG

# for messaging
from utilitities.logging import LoggingMixin
from django.contrib import messages



def home(request):
    return render(request=request,template_name='index.html',content_type='text/html',context={})

def verify_mail(request):
    return render(request=request,template_name='admin-otp.html',content_type='text/html',context={})


def exam_onboarding(request):
    return render(request=request,template_name='exam-onboarding.html',content_type='text/html',context={})

def login(request):
    if request.method == "POST":
        user_id = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            # Fetch the user by user_id
            user = CustomUser.objects.get(user_id=user_id)

            # Verify the password
            if user.check_password(password):
                if user.is_superuser: #check if is_super user

                    otp = get_otp() # call the get_otp() function to get the opt
                    
                    if DEBUG:
                        LoggingMixin(message=f"Your OTP is :{otp}. It will expire in {OTP_EXPIRATION_TIME}").log()
                        return  redirect('verify_mail')
                    else:
                        try:
                            otp_email = EmailSender(subject='Login OTP')
                            # call the send_otp_email method to actually do the email sending
                            otp_email.send_otp_email(email=user.email, first_name=user.first_name, otp_code=otp,time = OTP_EXPIRATION_TIME)
                            return redirect('')
                        except Exception as e:
                            return   redirect('verify_mail')

                elif user.is_student and user.is_active:
                    LoggingMixin(f'Successfully Logged in as {user.first_name}').log()
                    return  redirect('exam_onboarding')  
            LoggingMixin('Either UserID or Password is incorrect').log()
            messages.error(request,"Either UserID or Password is incorrect")
            return render(request=request,template_name="index.html",content_type='text/html',context= {})
        except CustomUser.DoesNotExist:
            LoggingMixin('Either UserID or Password is incorrect').log()
            messages.success(request,message="Either UserID or Password is incorrect")
            return render(request=request,template_name="index.html",content_type='text/html',context= {})
    else:
        return render(request=request,template_name='index.html',content_type='text/html',context={})