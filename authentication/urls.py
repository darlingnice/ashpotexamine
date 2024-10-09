from django.urls import path
from . import views


urlpatterns =[
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('verify-email',views.verify_mail,name='verify_mail'),
    path('onboarding/',views.exam_onboarding,name='exam_onboarding')
]