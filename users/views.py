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

from blogs.views import *


def all_banner(request):
    all_ban = Banner.objects.all()
    return all_ban

def Home(request):
    banner_data = all_banner(request)
    product_list = top_products(request)
    old_products  = feature_products(request)
    t_brands = top_brands(request)
    t_blogs = top_blogs(request)
    # print(product_list) 
    return render(
        request,
        'home/index.html',
        {
            'product_list':product_list,
            'banner_data':banner_data,
            'old_products':old_products,
            't_brands':t_brands,
            't_blogs':t_blogs
        })


def about(request):
    return render(request,'home/about.html')

def faq(request):
    return render(request,'home/faq.html')

def contact(request):
    return render(request,'home/contact.html')

    
# Create your views here.
def users(request):
    if request.user.is_authenticated:
        return redirect('users:Signin')
    else:
        return redirect('users:Signin')


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
                return redirect('users:Signin')       
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