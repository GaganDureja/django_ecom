from django.contrib import admin
from . models import *
# Register your models here.
class CategoryListing(admin.ModelAdmin):
    model = Category
    list_display = ['pk', 'name', 'created_on', 'updated_on']

class TagListing(admin.ModelAdmin):
    model = Tag
    list_display = ['pk', 'name', 'created_on', 'updated_on']

class BlogListing(admin.ModelAdmin):
    model = Blog
    list_display = ['pk', 'category', 'heading', 'created_on', 'updated_on']
   
admin.site.register(Category,CategoryListing)
admin.site.register(Tag,TagListing)
admin.site.register(Blog,BlogListing)