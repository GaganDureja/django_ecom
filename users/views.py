from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader

from django.utils import timezone
import datetime
from django.contrib import messages


from .models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login, logout 

# Create your views here.
from products.views import *

def all_banner(request):
    all_ban = Banner.objects.all()
    return all_ban

def Home(request):
    banner_data = all_banner(request)
    product_list = top_products(request)
    # print(product_list) 
    return render(request,'home/index.html',{'product_list':product_list,'banner_data':banner_data})





    
# Create your views here.
def users(request):
    x = "Time now (UTC): ", timezone.now()
    y = "Localtime (Timezone time):" , timezone.localtime()
    z = "Localmachine (default local) :" , datetime.datetime.now()
    my_dict = {'x':{'a':1,'b':50},'y':1,'z':1}
    # return HttpReponse(my_list)
    # return redirect('home')

    # print(my_dict,'cccccccc')
    
    # return render(request,'users/index.html',my_dict)

    # return HttpResponse("Hello this is users index!")


    all_users = User.objects.all()

    # print(all_users)

    return render(request,'users/index.html',{'all_users':all_users})


def Signup(request): 
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('home')
    else:   
        if request.method == 'GET':
            return render(request,'home/account.html')
        if request.method == 'POST':
            
            if User.objects.filter(email=request.POST.get('email')):
                messages.warning(request, "User already exists with this email")
                return redirect('users:Signup')
            
            User.objects.create(
                password = make_password(request.POST.get('password_in_2')),
                username= request.POST.get('email'),
                first_name = request.POST.get('fname'),
                last_name= request.POST.get('lname'),
                email=request.POST.get('email')
            )

            messages.success(request, "User registered successfully!")
            return redirect('users:Signup')
        

def Signin(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request,'home/account.html')
        if request.method == 'POST':
            if User.objects.filter(email=request.POST.get('email')):
                user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password_in'))
                if user:
                    login(request, user)    
                    messages.success(request, "Login success")
                    return redirect('home')
                else:
                    messages.error(request, "Incorrect password!!!")
                # if User.objects.filter(email=request.POST.get('email'),password=make_password(request.POST.get('password_in'))):
                #     if User.objects.filter(email=request.POST.get('email'),password=make_password(request.POST.get('password_in')),is_active=1):
                #         messages.success(request, "Login success")
                #         return render(request,'home/account.html')
                #     else:
                #         messages.warning(request, "Account Deactivated!!!")
                # else:
                #     messages.error(request, "Incorrect password!!!")     
                return redirect('users:Signin')       
                return render(request,'home/account.html')
            else:
                messages.warning(request, "Email not registered")      
                return render(request,'home/account.html')
        

# logout page
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout success")
    else:
        messages.warning(request, "Already Logged out")
    return redirect('users:Signin')