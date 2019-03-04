from django.contrib import admin
from .models import Group, Gender, Country, Merchant, Profile, Product, Order, Status

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','gender','country','funds')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'code', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','merchant_id','price','size')

admin.site.register(Group)
admin.site.register(Gender)
admin.site.register(Country)
admin.site.register(Merchant)
admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Status)
