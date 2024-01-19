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



from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json

import random






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
    if not total_price:
        messages.warning(request, "No items in cart")
        return redirect('view_cart')

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
    address_id = request.POST.get('address_id')
    shipping = request.POST.get('shipping')
    if not address_id:
        messages.warning(request, "Please select delivery address")
        return redirect('checkout')
    elif Address.objects.filter(id=address_id):
        # proceed payment
        return render(request,'home/proceed-payment.html', {'address_id':address_id,'shipping':shipping})
    else:
        messages.warning(request, "Address not found")
        return redirect('checkout')



@csrf_exempt
def create_checkout_session(request): 
    stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"
    
    try:        
        request_data = json.loads(request.body)        
        address_id = request_data['address_id']
        shipping = request_data['shipping']
        if shipping=='1':
            shipping_price = 0
            shipping_desc = 'Normal Delivery'
        else:
            shipping_price = 100
            shipping_desc = 'Express Delivery'
        
        

        user_cart,created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        
        total_price = sum(item.total_price() for item in cart_items)
        # get address details 
        address_det = get_object_or_404(Address,id=address_id)
        order_id = "ecom"+ str(random.randint(111111111, 999999999))
        if total_price:
            checkout_session = stripe.checkout.Session.create(        
                customer_email = request.user.email,           
                payment_method_types = ['card'],
                line_items = [
                    
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': item.product,
                                'description':item.product.brand
                            },
                            'unit_amount': item.product.price*100,
                        },
                        'quantity': item.quantity,
                    } for item in cart_items
                ] + [
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': 'Shipping',
                                'description': shipping_desc,
                            },
                            'unit_amount': shipping_price * 100,
                        },
                        'quantity': 1,
                    }
                ],
                mode = 'payment',            
                success_url = request.build_absolute_uri(reverse(payment_details)) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url = request.build_absolute_uri(reverse(payment_details)) + "?session_id={CHECKOUT_SESSION_ID}",
                metadata={
                    'order_id': order_id,
                },
                # customer={
                #     'name': address_det.full_name,
                #     'email': request.user.email,
                #     'phone': address_det.phone,
                #     'address': {
                #         'line1': address_det.house_building + ', ' + address_det.road_area + ', ' + address_det.nearby + ' (' + address_det.address_type + ')',
                #         'city':  address_det.city,
                #         'postal_code':  address_det.pincode,
                #         'state':  address_det.state,
                #         'country': 'IN',
                #     },
                #     'metadata': {
                #         'order_id': order_id,
                #     },
                # },
            )
            # save order details
            create_order = Order.objects.create(
                order_id = order_id,
                full_name = address_det.full_name,
                phone = address_det.phone,
                alt_phone = address_det.alt_phone,
                pincode = address_det.pincode,
                state = address_det.state,
                city = address_det.city,
                house_building = address_det.house_building,
                road_area = address_det.road_area,
                nearby = address_det.nearby,
                address_type = address_det.address_type,
                shipping_charge = shipping_price,
                total_price = total_price,
                user = request.user
            )
            
            # add order items
            for item in cart_items:
                OrderItem.objects.create(
                    product = item.product,
                    quantity = item.quantity,
                    sub_total = item.quantity * item.product.price,
                    order=create_order
                )
            
            # delete cart
            Cart.objects.filter(user=request.user).delete()

            # print(checkout_session)
            return JsonResponse({'sessionId': checkout_session.id})
        else:
            messages.warning(request, "No items in cart")
            return redirect('view_cart')
        
    except Exception as e:
        messages.warning(request, "No items in cart")
        return redirect('view_cart')
        # return JsonResponse({'error': str(e)}, status=500)
        


@login_required
def payment_details(request):
    session_id = request.GET.get('session_id')
    
    if session_id:
        stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"

        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            order_id = checkout_session.metadata.get('order_id')
            payment_intent_id = checkout_session.payment_intent
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            # You can now access various details from the payment_intent object

            # Extract specific details
            payment_status = payment_intent.status
            payment_amount = payment_intent.amount_received / 100  # Convert from cents to your currency
            
            Order.objects.filter(order_id=order_id).update(payment_id=payment_intent.client_secret)
            if payment_status == "succeeded":
                messages.success(request, "Order Successful")
                Order.objects.filter(order_id=order_id).update(payment_status=1)

                
            
            

            return render(request, 'home/payment-details.html', {
                'payment_status': payment_status,
                'payment_amount': payment_amount,
                'payment_intent': payment_intent,
                'order_id': order_id
            })

        except stripe.error.StripeError as e:
            # Stripe errors
            return render(request, 'home/payment-details.html', {'error': str(e)})

    else:
        # no session_id
        return HttpResponse("Invalid request. Missing session_id.")


@login_required
def orders_list(request):
    my_order = Order.objects.filter(user=request.user)
    return render(request, 'home/orders.html', {'my_order': my_order})

def order_details(request,order):
    # order_id = request.GET.get('order')
    order_det = get_object_or_404(Order, order_id=order)
    if order_det:
        return render(request, 'home/order-details.html', {'order_det': order_det})
    else:
        return redirect(orders_list)


    

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









