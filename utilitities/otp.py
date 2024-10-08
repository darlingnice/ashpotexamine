import pyotp
import qrcode
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

key = "telltheworldthatthekingdomofGodishere"
code = pyotp.TOTP(key)

def get_otp():
    return code.now()


def verify_otp_code(otp):
    return code.verify(otp,valid_window=1)


OTP_EXPIRATION_TIME = '90 seconds'