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
from django.core.exceptions import ValidationError


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



@login_required
def view_address(request):
    user_add = Address.objects.filter(user=request.user).values()
    if(user_add):
        response_data = {'success': True, 'message': list(user_add)}
    else:
        response_data = {'success': False, 'message': 'No Address found'}
    return JsonResponse(response_data)
    # return {'user_add':user_add}
    

@login_required
def add_address(request):
    if request.method == 'POST':        
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode'),
        state = request.POST.get('state'),
        city = request.POST.get('city'),
        house_building = request.POST.get('house_building'),
        road_area = request.POST.get('road_area')

        if not (full_name and phone and pincode and state and city and house_building and road_area):
            response_data = {'success': False, 'message': 'Invalid form data'}
            return JsonResponse(response_data, status=400)

        

        try:
            Address.objects.create(
                user = request.user,
                full_name = request.POST.get('full_name'),
                phone = request.POST.get('phone'),
                alt_phone = request.POST.get('alt_phone'),
                pincode = request.POST.get('pincode'),
                state = request.POST.get('state'),
                city = request.POST.get('city'),
                house_building = request.POST.get('house_building'),
                road_area = request.POST.get('road_area'),
                nearby = request.POST.get('nearby'),
                address_type = request.POST.get('address_type'),
            )
            response_data = {'success': True, 'message': 'Address saved successfully'}
            return JsonResponse(response_data)
        except ValidationError as e:
                response_data = {'success': False, 'message': f'Validation error: {str(e)}'}
                return JsonResponse(response_data, status=400)
        except Exception as e:
            response_data = {'success': False, 'message': f'Error saving address: {str(e)}'}
            return JsonResponse(response_data, status=500)
    else:
        response_data = {'success': False, 'message': 'Invalid request method'}
        return JsonResponse(response_data, status=405)
    

import stripe
@login_required
def payment(request):
    stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"

    token = request.POST.get("stripeToken")
    amount = 1000  # Amount in cents

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            description="Payment for your product or service",
        )

        # Process successful payment (update database, send confirmation email, etc.)
        # ...

        return JsonResponse({'success': True, 'message': 'Payment successful'})

    except stripe.error.CardError as e:
        return JsonResponse({'success': False, 'message': f'Card error: {e.error.message}'}, status=400)

    except stripe.error.StripeError as e:
        return JsonResponse({'success': False, 'message': f'Payment failed: {e.error.message}'}, status=500)

def Signup(request): 
    next_url =  request.POST.get('next')
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
            if next_url:
                return redirect(next_url)
            else:
                return redirect('users:Signup')
        

def Signin(request):
    next_url =  request.POST.get('next')
    
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
                        return redirect(next_url)
                    else:
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




def order_details(request):
    return render(request,'home/order-details.html')



# from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json

@csrf_exempt
def create_checkout_session(request): 
    request_data = json.loads(request.body)
    print(request_data)
    aa = request_data['aa']
    print(aa)
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"

    checkout_session = stripe.checkout.Session.create(        
        customer_email = request.user.email,
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': 'product_name',
                    },
                    'unit_amount': int(400)*100,
                },
                'quantity': 1,
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse('home')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('checkout')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    # order = Order()
    # # order.customer.email = request_data['email']
    # order.product = product
    # order.customer=customer[0]
    # order.stripe_payment_intent = checkout_session['payment_intent']
    # order.price = int(product.price * 100)
    # order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})
