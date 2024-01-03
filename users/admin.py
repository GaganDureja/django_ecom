from django.contrib import admin
from .models import *
# Register your models here.




# class UserListing(admin.ModelAdmin):
#     model = User
#     list_display = ['pk', 'username', 'first_name', 'last_name']

class UserListing(admin.ModelAdmin):
    model = User
    list_display = ['s_no', 'username', 'first_name', 'last_name']

        
    def s_no(self, obj):        
        return User.objects.count() - User.objects.filter(pk__lte=obj.pk).count() + 1
    s_no.short_description = 'S.no'  # Column header in admin panel

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(User,UserListing)
# admin.site.register(all_field)