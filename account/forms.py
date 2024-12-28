from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile,SellerProfile,CustomUser

class CustomerCreationForm(UserCreationForm):
    class Meta: 
        model = CustomerProfile
        fields = ['username', 'first_name','last_name','contact','email','dob','gender','profile_picture']
        

class SellerCreationForm(UserCreationForm):
    class Meta: 
        model = SellerProfile
        fields = ['username', 'first_name','last_name','contact','email','business_name','business_address','business_pincode','business_landmark','product_category','business_website']


from django import forms

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(label="Enter your registred email")
