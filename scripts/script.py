from authentication.models import CustomUser
from django.contrib.auth.hashers import make_password

def run():
    user = CustomUser()
    user.is_active = True
    user.first_name ='Bianca'
    user.password = make_password("tryandsee12345")
    user.last_name = "Ngozi"
    user.is_student = True
    user.user_id = "ASHPOT2024/003"
    user.email = "biancang@gmail.com"
    user.save()
    print("user saved")