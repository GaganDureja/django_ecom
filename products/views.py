from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import *




# Create your views here.
def cat_links(request):
    all_categories = category.objects.all()

    categories_with_subcategories = []
    for cat in all_categories:
        subcategories = sub_category.objects.filter(category=cat)
        categories_with_subcategories.append({'category': cat, 'subcategories': subcategories})

    return categories_with_subcategories
    


def top_products(request):
    all_products = product.objects.all()[:8]
    return all_products
    # return render(request,'products/products.html',{'all_products':all_products})


def products(request, category_slug=None, sub_category_slug=None):
    all_products = product.objects.all()
    # if category:
    #     all_products = all_products.filter(category=category)
    # if sub_category:
    #     all_products = all_products.filter(sub_category=sub_category)

    cat = None
    subcat = None
    
    if category_slug:
        cat = get_object_or_404(category, slug=category_slug)
        all_products = all_products.filter(category=cat)
        if sub_category_slug:
            subcat = get_object_or_404(sub_category, slug=sub_category_slug)
            all_products = all_products.filter(sub_category=subcat)

    
    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 6)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/products.html', {'all_products': products})
