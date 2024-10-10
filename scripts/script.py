from authentication.models import CustomUser
from django.contrib.auth.hashers import make_password

def run():

    user_id = "ASHPOT2024/002"
    try:
        CustomUser.objects.get(user_id=user_id)
        print("User already exixts")
        
    except CustomUser.DoesNotExist:
        user = CustomUser()
        user.is_active = True
        user.first_name ='Jay'
        user.password = make_password("tryandsee12345")
        user.last_name = "Tina"
        user.is_student = True
        user.user_id =user_id
        user.email = "jay@gmail.com"
        
        user.save()    
        print("user saved")