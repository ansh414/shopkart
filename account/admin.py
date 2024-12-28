from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerProfile,SellerProfile,CustomUser,Category,Product,Cart,Shipping_Address,Order,OrderItem

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['username','first_name','last_name','email','contact','is_staff']
admin.site.register(CustomUser,CustomUserAdmin)

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['dob','gender','profile_picture']
admin.site.register(CustomerProfile,CustomerProfileAdmin)


class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name','business_address','business_pincode','business_landmark','business_website','product_category']
admin.site.register(SellerProfile,SellerProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','description','price','category','stock_qty','created_at','updated_at','image']
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id','customer','quantity','product']
admin.site.register(Cart,CartAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display=['id','customer','address_line1','landmark','city','state','pincode']
admin.site.register(Shipping_Address,ShippingAddressAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','customer','order_date','shipping_address','payment_status','order_status','order_amount']
admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','unit_price']
