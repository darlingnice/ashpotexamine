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
from exam.models import ScheduledExam
import os
from exam.models import Question
import random

    # Initializes list for shuffled questions
list_of_exam_shuffled_questions_number = []


def home(request):
    return render(request=request,template_name='index.html',content_type='text/html',context={})

def verify_mail(request):
    return render(request=request,template_name='admin-otp.html',content_type='text/html',context={})

# def exam_onboarding(request, id):

#     # Fetch all question IDs
#     qtns = Question.objects.all()
#     lst = [q.id for q in qtns]
    
#     # Shuffle the list of question IDs
#     random.shuffle(lst)
#        # Fetch scheduled exam info
#     info = ScheduledExam.objects.filter(id=id).first()
#     # Add the shuffled question IDs to list_of_exam_shuffled_questions_number
#     global list_of_exam_shuffled_questions_number
#     list_of_exam_shuffled_questions_number = lst[:info.num_questions ]


#     if info is None:
#         return render(request=request, template_name='exam-onboarding.html', content_type='text/html', context={"schedule": info})


#     return render(request=request,template_name='exam-onboarding.html',content_type='text/html',context={"schedule":info,'id':info.id})

    # # Pass the shuffled questions to the template or use them as needed
    # return render(request, 'exam-onboarding.html', context={"schedule": info, "shuffled_questions": list_of_exam_shuffled_questions_number})




def exam_onboarding(request,id):
   
    info = ScheduledExam.objects.filter(id =id).first()
    if info is None :
        return render(request=request,template_name='exam-onboarding.html',content_type='text/html',context={"schedule":info})
   
    #  Fetch all question IDs
    qtns = Question.objects.all()
    lst = [q.id for q in qtns]

    # Shuffle the list of question IDs
    random.shuffle(lst)
    for x in lst[:info.num_questions]:
        list_of_exam_shuffled_questions_number.append(x)
    print(list_of_exam_shuffled_questions_number)    
    return render(request=request,template_name='exam-onboarding.html',content_type='text/html',context={"schedule":info,'id':info.id})


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
                            messages.success(request=request,message=f"OTP sent to {user.email}")
                            return redirect('verify_mail')
                            
                        except Exception as e:
                            LoggingMixin(f"Error occured while sending mail :{e}")
                            messages.success(request=request,message=f"{e}")
                            return render(request=request,template_name='index.html',content_type='text/html',context={})

                elif user.is_student and user.is_active:
                    LoggingMixin(f'Successfully Logged in as {user.first_name}').log()
                    # get the scheduled exam information
                    user = CustomUser.objects.filter(user_id=user_id).first()
                    record= ScheduledExam.objects.filter(user =user).first()
                    if record:
                        info = record.pk
                    else:
                        info = 0    

                    return  redirect('exam_onboarding',info)  
            LoggingMixin('Either UserID or Password is incorrect').log()
            messages.error(request,"Either User ID or Password is incorrect")
            return render(request=request,template_name="index.html",content_type='text/html',context= {})
        except CustomUser.DoesNotExist:
            LoggingMixin('Either User ID or Password is incorrect').log()
            messages.success(request,message="Either User ID or Password is incorrect")
            return render(request=request,template_name="index.html",content_type='text/html',context= {})
    else:
        return render(request=request,template_name='index.html',content_type='text/html',context={})