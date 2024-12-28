from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,RegexValidator
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    contact = models.CharField(max_length=10,validators=[RegexValidator(regex=r'^\d{10}$',message='contact number must be exactly of 10 digits')])
    # user_type = models.CharField(max_length=10,choices=(('seller','Seller'),('customer','Customer')),default='customer')
    groups = models.ManyToManyField('auth.Group',related_name='account_user_set',blank=True)
    user_permissions=models.ManyToManyField('auth.Permission',related_name='account_user_permission_set',blank=True)

    def __str__(self):
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

class CustomerProfile(CustomUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customer_profile')
    dob = models.DateField()
    gender = models.CharField(max_length=10,choices=(('male','Male'),('female','Female')))
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True,blank=True)

    class Meta:
        db_table = 'CustomerProfile'
    
PRODUCT_CATEGORY_CHOICES = [
        ('electronics', 'ELECTRONICS'),
        ('fashion', 'FASHION'),
        ('home_appliances', 'HOME_APPLIANCES'),
        ('books', 'BOOKS'),
        ('beauty', 'BEAUTY'),
        ('sports', 'SPORTS'),
        ('toys', 'TOYS'),
        ('mobile_and_tablets', 'MOBILE AND TABLETS'),
        ('home_and_kitchen','HOME AND KITCHEN'),
        ('other', 'OTHER'),
    ]

class SellerProfile(CustomUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=6,validators=[RegexValidator(regex=r'^\d{6}$',message='enter valid 6 digits pincode')])
    business_landmark = models.CharField(max_length=255)
    product_category = models.CharField(max_length=50, choices=PRODUCT_CATEGORY_CHOICES)
    business_website = models.URLField(null=True,blank=True)

    class Meta:
        db_table = 'SellerProfile'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock_qty = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True) 
    # auto_now_add = fixed date
    updated_at = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Shipping_Address(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6,validators=[RegexValidator(r'\d{6}$','Enter a valid 6 digit pincode')])

    
class Order(models.Model):
    order_id = models.CharField(max_length=50,primary_key=True)
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    shipping_address = models.ForeignKey(Shipping_Address,on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20,choices=(('paid','Paid'),('unpaid','Unpaid')),default='unpaid')
    order_status = models.CharField(max_length=20,choices=(('pending','Pending'),('shipped','Shipped'),('delivered','Delivered')),default='pending')
    order_amount=models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)

    