from pyexpat import model
#from attr import field
from django.forms import ModelForm
from .models import Category, Seller, Product, Cart
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
class NewForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = ['brand','type','address']
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields="__all__"   
        exclude=['seller']

