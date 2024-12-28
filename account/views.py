import datetime
import random
from django.shortcuts import get_object_or_404, render,redirect
from .models import CustomerProfile, CustomUser, SellerProfile,Product,Category,Cart,Shipping_Address,Order,OrderItem
from .forms import CustomerCreationForm,SellerCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout

# Create your views here.
def index(request):
    products = Product.objects.all()
    context={
        'products':products
    }
    return render(request,"index.html",context)


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = "Something went wrong"
            return render(request,'customer_signup.html',{'error':error,'form':form})

    else:
        form = CustomerCreationForm()
    return render(request,"customer_signup.html",{'form':form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerCreationForm(request.POST,request)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = "Something went wrong"
            return render(request,'seller_signup.html',{'error':error,'form':form})

    else:
        form = SellerCreationForm()
    return render(request,"seller_signup.html",{'form':form})



def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('index')
        else:
            return render(request,"signin.html",{'form':form})

    else:
        form = AuthenticationForm()
    return render(request,"signin.html",{'form':form})


def signout(request):
    logout(request)
    return redirect('index')

def category(request):
    cat_name = request.GET.get('product') #The product is coming from the url string "?produc" under base.html
    cat_object = Category.objects.get(name=cat_name)
    sort_option = request.GET.get('sort')
    products = Product.objects.filter(category=cat_object)
    if sort_option == 'lth':
        products = products.order_by('price')
    elif sort_option == 'htl':
        products = products.order_by('-price')
    context={
        'products':products,
        'category':cat_object
    }
    return render(request,"index.html",context)

def search_product(request):
    value = request.GET.get('search_bar') #search_bar id defined in the url in base.html header section
    products = Product.objects.none()

    if value is not None:
        category = Product.objects.filter(category__name__icontains=value) # To understand this check Django Lookups
        title = Product.objects.filter(title__icontains=value)
        description = Product.objects.filter(description__icontains=value)

    products = category | title | description

    context={
    'products':products
    }
    return render(request,"index.html",context)

def product_details(request,id):
    product = Product.objects.get(id=id)
    date = datetime.datetime.today().date()+datetime.timedelta(days=5)
    context = {
        'product':product,
        'date': date
    }
    return render(request,"product_details.html",context)


def addtocart(request,id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.get(id=request.user.id)
    else:
        return redirect('signin')
    
    cart_item,created = Cart.objects.get_or_create(product=product,customer=customer)

    if not created:
        cart_item.quantity+=1
    else:
        cart_item.quantity=1

    cart_item.save()
    return redirect('cart')

def cart(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(customer = request.user)
    else:
        return redirect('signin')
    
    total_amount = 0
    for item in cart_item:
        total_amount+= item.product.price*item.quantity

    context = {
            'items':cart_item,
            'total_amount':total_amount,
            'total_product':len(cart_item)
        }
    return render(request,"cart.html",context)


def updateqty(request,id):
    cart_item = Cart.objects.get(product=id, customer=request.user)
    val = request.GET.get('val')
    if val == '0':
        if cart_item.quantity>1:
            cart_item.quantity-=1
    else:
        cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')

def remove_item(request,id):
    cart_item = Cart.objects.get(product=id, customer=request.user)
    cart_item.delete()
    return redirect('cart')

def address(request):
    if request.method=='POST':
        address_line = request.POST['address']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        user = CustomerProfile.objects.get(id=request.user.id)
        address = Shipping_Address.objects.create(customer=user,address_line1=address_line,landmark=landmark,city=city,state=state,pincode=pincode)
        address.save()
        return redirect('address')
    else:
        address = Shipping_Address.objects.filter(customer=request.user)

    context={
        'address':address
    }
    return render(request,'address.html',context)

def remove_address(request,id):
    address = Shipping_Address.objects.get(id=id)
    address.delete()
    return redirect('address')

def update_address(request,id):
    update_address = Shipping_Address.objects.get(id=id)
    addresses = Shipping_Address.objects.filter(customer=request.user)
    if request.method=='POST':
        update_address.address_line1 = request.POST['address']
        update_address.landmark = request.POST['landmark']
        update_address.city = request.POST['city']
        update_address.state = request.POST['state']
        update_address.pincode = request.POST['pincode']
        update_address.save()
        return redirect('address')
    context={
        'address':addresses,
        'update_address':update_address
    }
    return render(request,'address.html',context)

def confirm_order(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(customer = request.user)
        address = Shipping_Address.objects.get(id=id)
        total_amount=0
        for item in cart_item:
            total_amount += item.product.price*item.quantity

        context={
            'cart_items':cart_item,
            'total_amount':total_amount,
            'address':address
        }

        return render(request,"confirm_order.html",context)
    
    else:
        return redirect('signin')
    

import random
import razorpay

def pay(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(customer = request.user)
        address = Shipping_Address.objects.get(id=id)
        total_amount=0
        for item in cart_item:
            total_amount += item.product.price*item.quantity

        order_id = random.randrange(1000,99999)
        customer = CustomerProfile.objects.get(id=request.user.id)
        date=datetime.datetime.today().date()
        order = Order.objects.create(order_id=order_id,customer=customer,order_date=date,shipping_address=address,order_amount=total_amount)

        order.save()
        for item in cart_item:
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,unit_price=item.product.price)
        cart_item.delete()

    client=razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ","UOrbXQGnsEc2dhB1IFg0zNWZ"))
    data={"amount":int(total_amount*100),"currency":"INR","receipt":str(order_id)}
    payment=client.order.create(data=data)

    context={
        'data':data,
        'payment':payment
    }
        
    return render(request,'pay.html',context)

def payment_success(request):
    payment_id = request.GET.get('payment_id','N/A')
    order_id = request.GET.get('order_id','N/A')
    order = get_object_or_404(Order,order_id=order_id)

    #Update the payment status
    order.payment_status = 'paid'
    context={
        'payment_id':payment_id,
        'order_id':order_id
    }
    order.save()
    return render(request,'payment_success.html',context)

from .forms import PasswordResetEmailForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(user):
    otp = str(random.randint(100000,999999))
    return otp

def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp(user)

                request.session['otp'] = otp
                request.session['request_user'] = user.id

                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is : {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return redirect('verify_otp')
            except CustomUser.DoesNotExist:
                messages.error(request,"No user found with this email")
                return render(request,'forgot_password.html',{'form':form})
            
    else:
        form = PasswordResetEmailForm()
    return render(request,'forgot_password.html',{'form':form})
    
def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        otp_stored = request.session['otp']

        if otp_entered == otp_stored:
            user_id = request.session['request_user']
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                return redirect('reset_password',user_id=user.id)
            else:
                messages.error(request,"Session Expired please request for otp again")
                return redirect('forgot_password')
        else:
            messages.error(request,"Invalid OTP")
            return render(request,'verify_otp.html')

    return render(request,'verify_otp.html')

from django.contrib.auth.forms import SetPasswordForm

def reset_password(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        form = SetPasswordForm(user=user,data=request.POST)
        if form.is_valid():
            form.save()

            if 'otp' in request.session:
                del request.session['otp']
            
            if 'request_user' in request.session:
                del request.session['request_user']

            messages.success(request,"Your password has been reset successfully")
            return redirect('signin')
        
    else:
        form = SetPasswordForm(user=user)
    return render(request,'reset_password.html',{'form':form})

