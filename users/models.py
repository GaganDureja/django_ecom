from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from products.models import product

class User(AbstractUser):
    pass




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        else:
            return f"Anonymous Cart ({self.session_key})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

    def total_price(self):
        return self.quantity * self.product.price


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=55)
    phone = models.CharField(max_length=15)
    alt_phone = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    house_building = models.CharField(max_length=255)
    road_area = models.CharField(max_length=255)
    nearby = models.CharField(max_length=255, null=True, blank=True)
    address_type = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=55)
    phone = models.CharField(max_length=15)
    alt_phone = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    house_building = models.CharField(max_length=255)
    road_area = models.CharField(max_length=255)
    nearby = models.CharField(max_length=255, null=True, blank=True)
    address_type = models.CharField(max_length=5)
    total_price = models.PositiveIntegerField(default=1)
    payment_id = models.CharField(max_length=155, null=True, blank=True)
    payment_status = models.BinaryField(default=0, null=True)
    admin_status = models.BinaryField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.user:
            return f"Order for {self.user.username}"
        else:
            return f"Anonymous Order"
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order}"

    

 