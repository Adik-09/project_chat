from django.urls import path
from .views import *

urlpatterns = [
    path('ak/register/',register,name='register-page'),
    path('ak/login/',user_login,name='login-page'),
    path('ak/forget_pass/',forget_pass,name='forget-page'),
    path('ak/verify_otp/',verify_otp,name='verify-otp'),
    path("ak/change_password/",change_password, name="change-password"),
    path('ak/logout/',user_logout),
]
