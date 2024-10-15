from authentication.models import CustomUser
from django.contrib.auth.hashers import make_password

def run():

    user_id = "ASHPOT2024/001"
    try:
        CustomUser.objects.get(user_id=user_id)
        print("User already exixts")
        
    except CustomUser.DoesNotExist:
        user = CustomUser()
        user.is_active = True
        user.first_name ='Darlington'
        user.password = make_password("tryandsee12345")
        user.last_name = "Urom"
        user.is_student = True
        user.user_id =user_id
        user.email = "darlington@gmail.com"
        
        user.save()    
        print("user saved")