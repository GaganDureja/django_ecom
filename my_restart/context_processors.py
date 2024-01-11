# myproject/context_processors.py

from products.models import category, sub_category  # Adjust this import based on your app's structure

from users.models import Cart, CartItem

def global_categories(request):
    all_categories = category.objects.all()
    
    categories_with_subcategories = []
    for cat in all_categories:
        subcategories = sub_category.objects.filter(category=cat)
        categories_with_subcategories.append({'category': cat, 'subcategories': subcategories})

    return {
        'categories_with_subcategories': categories_with_subcategories,
    }


def cart_items(request):
    if not request.user.is_authenticated:
        cart_items_top = ""
    else:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_top = CartItem.objects.filter(cart=user_cart)
        total_price = sum(item.total_price() for item in cart_items_top)
    return {
        'cart_items_top': cart_items_top,
        'total_cart_items': cart_items_top.count(),
        'cart_total_price': total_price,
    }