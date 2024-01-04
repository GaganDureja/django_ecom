from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(title_links)

class CategoryListing(admin.ModelAdmin):
    model = category
    list_display = ['pk', 'name', 'created_on', 'updated_on']

class SubcatListing(admin.ModelAdmin):
    model = sub_category
    list_display = ['pk','category', 'name', 'created_on', 'updated_on']

class BrandListing(admin.ModelAdmin):
    model = brand
    list_display = ['pk', 'name', 'created_on', 'updated_on']

class ProductListing(admin.ModelAdmin):
    model = product
    list_display = ['pk','category','sub_category', 'name', 'created_on', 'updated_on']

class BannerListing(admin.ModelAdmin):
    model = Banner
    list_display = ['pk', 'heading', 'created_on', 'updated_on']
   
admin.site.register(category,CategoryListing)
admin.site.register(sub_category,SubcatListing)
admin.site.register(brand,BrandListing)
admin.site.register(product,ProductListing)
admin.site.register(Banner,BannerListing)
admin.site.register(P_Images)