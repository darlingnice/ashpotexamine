from rest_framework.serializers import ModelSerializer
from authentication.models import CustomUser
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model =CustomUser
        fields = ['user_id','password','email']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'email':{'read_only':False}
        }