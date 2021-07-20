from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .serializers.serializer import *
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout


# CLASS BASED VIEWS

# POSITIVE
# More advantage of Class based Views over Functional View are, it written in less lines of code. Because most of the functionalites are prebuild onto class view from Django.

# NEGATIVE
# Django possess a certain structure to build a class view so, it can only be build using those parameters.

#method_decorator is a decorator in django used for adding an addition features to a fuction.
#Here csrf_exempt used to add CSRF Token to the request. This technique of generating csrf on backed is used while working with api's
@method_decorator(csrf_exempt,name='dispatch')

#Below is how we write function in Python. Here we use a technique called Inheritence. Below class is inherited from Django's inbuild class View. 
class RegisterUser(View):

    #Below __int__ is called a constructor. In Django 1 of the most commonly used constructor is __init__ which basically named as Initializer
    def __init__(self):
        #Here self keword is used to represent the instance of the class
        self.template = 'register_user.html'

    def get(self, request):

        #render as name implies it renders the templates on the request.
        return render(request,self.template)


    def post(self, request):

        context = {}
        #below 3 lines are only used for Demo, when comes to api integration it wound work. The data from frontend should be parsed.
        context['first_name'] = request.POST.get('first_name')
        context['last_name'] = request.POST.get('last_name')
        context['email'] = request.POST.get('email')

        # Below JSONParser function used to parse datas send from frontend and only works with api
        # data = JSONParser().parse(request)

        #Here below JsonResponse helps to return a json response which will be in the form of a key value pair
        # eg:- {data:data}
        #Make sure safe parameter is always assigned as False, because by default it is True. If safe is set as True django won't allow to send a response back as the format we needed.
        return JsonResponse(context,safe=False, status=200)


# FUNCTIONAL BASED VIEW
#Render Template
def register_view_template(request):

    template = 'register_user.html'
    return render(request,template)

#Api EndPoint
@csrf_exempt
def register_view(request):

    if request.method == 'POST':
        context = {}
        context['username'] = request.POST.get('username')
        context['first_name'] = request.POST.get('first_name')
        context['last_name'] = request.POST.get('last_name')
        context['email'] = request.POST.get('email')
        context['password'] = request.POST.get('password')

        #Save to DB, Here we are using Django's inbuild model for saving user Details named User
        try:
            user = User.objects.get(username=context['username'],email=context['email'])

        except User.DoesNotExist:
            user = User.objects.create(username=context['username'],email=context['email'],
                            password=make_password(context['password']),first_name=context['first_name'],
                            last_name=context['last_name'])

        #Now, before sending a response back to frontend data should be serialized to a key value pair
        #So, we pass the query set onto a serializer and it converts to key value pair.
        token = Token.objects.get(user=user).key
        userSerializer = UserSerializer(user)

        return JsonResponse({"credentials":userSerializer.data,'token':token},safe=False, status=200)

    else:
        #if in case a GET request is send to this END Point, now it redirects to the Forms
        return redirect('register_user_function')


def login_user_template(request):
    template = 'login_user.html'

    return render(request,template)


@csrf_exempt
def login_user(request):

    user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))

    if user is not None:
        messages.success(request,'Success')
        login(request,user)
        userSerializer = UserSerializer(user)
        return JsonResponse({'credentials':userSerializer.data,'status':True},safe=False,status=200)

    else:
        messages.error(request,'Error')