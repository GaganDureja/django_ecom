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
    all_products = product.objects.all().order_by('-id')[:8]
    return all_products
    # return render(request,'products/products.html',{'all_products':all_products})

def feature_products(request):
    old_products = product.objects.all()[:8]
    return old_products

def top_brands(request):
    top_brand = brand.objects.all()
    return top_brand

def products(request, category_slug=None, sub_category_slug=None):
    all_products = product.objects.all()
    
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

    return render(request, 'products/products.html', {'all_products': products,'category':cat, 'subcategory':subcat})

def products1(request, category_slug=None, sub_category_slug=None):
    all_products = product.objects.all()
    
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

    return render(request, 'products/products1.html', {'all_products': products,'category':cat, 'subcategory':subcat})

from django.http import JsonResponse
from django.template.loader import render_to_string

def load_more_products(request):
    
    all_products = product.objects.all()
    
    cat = None
    subcat = None
    category_slug = request.GET.get('cat')
    sub_category_slug = request.GET.get('subcat')
    if category_slug:
        cat = get_object_or_404(category, slug=category_slug)
        all_products = all_products.filter(category=cat)
        if sub_category_slug:
            subcat = get_object_or_404(sub_category, slug=sub_category_slug)
            all_products = all_products.filter(sub_category=subcat)


    page = request.GET.get('page')
    products = product.objects.all()
    paginator = Paginator(products, 10)  # Adjust per_page as needed
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = []

    products_html = render_to_string('products/product_list_ajax.html', {'products': products})
    return JsonResponse({'products_html': products_html})

def product_detail(request, product_slug):
    product_det = get_object_or_404(product, slug=product_slug)
    related_pro = product.objects.filter(category=product_det.category)[:12]
    return render(request, 'products/product-detail.html',{'pro_det':product_det,'related_pro':related_pro})