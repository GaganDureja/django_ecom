from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone
import datetime
from django.contrib import messages

from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout 


from products.views import *
from blogs.views import *

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



def all_banner(request):
    all_ban = Banner.objects.all()
    return all_ban

def Home(request):
    banner_data = all_banner(request)
    product_list = top_products(request)
    old_products  = feature_products(request)
    t_brands = top_brands(request)
    t_blogs = top_blogs(request)
    

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


# def product_list(request):
#     products = product.objects.all()
#     return render(request, 'product_list.html', {'products': products})

@login_required
def view_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login Required")
        return redirect(Signup)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'home/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    c_product = get_object_or_404(product, pk=product_id)
    
    if not request.user.is_authenticated:
        messages.warning(request, "Login Required")
        return redirect(Signup)
    
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=c_product)
    
    messages.success(request, "Added to Cart!")
    if not created:        
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Cart updated!")
    referring_url = request.META.get('HTTP_REFERER', 'home')
    
    # Redirect back to the referring URL
    return redirect(referring_url)

@login_required
def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login Required")
        return redirect(Signup)
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()

    referring_url = request.META.get('HTTP_REFERER', 'home')
    
    # Redirect back to the referring URL
    return redirect(referring_url)



@require_POST
def update_cart_item(request, item_id, new_quantity):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()    
            
        new_subtotal = cart_item.product.price*new_quantity
        cart_items = CartItem.objects.filter(cart=cart_item.cart)
        total = sum(item.total_price() for item in cart_items)

        response_data = {'success': True, 'message': 'Quantity updated successfully','new_subtotal':new_subtotal,'total':total}
    except CartItem.DoesNotExist:        
        response_data = {'success': False, 'message': 'Cart item not found'}

    return JsonResponse(response_data)




@login_required
def checkout(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'home/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


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
    next_url =  request.GET.get('next')
    print(next_url)
    
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request,'home/account.html')
        if request.method == 'POST':            
            if User.objects.filter(email=request.POST.get('email')):
                user = authenticate(
                        request, 
                        username=request.POST.get('email'), 
                        password=request.POST.get('password_in')
                    )
                if user:
                    login(request, user)    
                    messages.success(request, "Login success")
                    if next_url:
                        print("yes next",next_url)
                        return redirect(next_url)
                    else:
                        print("no next",next_url)
                        return redirect('home')
                else:
                    messages.error(request, "Incorrect password!!!")
                return redirect('users:Signin')       
            else:
                messages.warning(request, "Email not registered")      
                return render(request,'home/account.html')
        

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout success")
    else:
        messages.warning(request, "Already Logged out")
    return redirect('users:Signin')