from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #Class View URL
    path('class/register-user/',RegisterUser.as_view(),name='register_user_class'),

    #Functional View URL
    path('function/register-user/',register_view_template,name='register_user_function'),

    #Functional API End Point
    #This url can't be accessed directly
    path('register/user/',register_view, name='register_user'),

    path('login/',login_user_template,name='login_user_view'),
    path('login_user/',login_user,name='login_user'),
    path('login/token/',obtain_auth_token,name='login_token')
]