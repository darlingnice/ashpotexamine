from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The user id field must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)      
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200,null=True,blank=True) 
    last_name = models.CharField(max_length=200,null=True,blank=True)
    email   = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'  # Use user_id for authentication
    REQUIRED_FIELDS = []  # No additional fields required

    def __str__(self):
        return self.user_id
   




