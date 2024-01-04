from django.urls import path
from . import views

app_name="products"

urlpatterns = [
    path('', views.products, name='product_list'),
    path('detail/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.products, name='product_list_category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/', views.products, name='product_list_subcategory'),
]