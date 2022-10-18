from datetime import datetime
from distutils.command.upload import upload
from email.headerregistry import Address
from email.policy import default
from multiprocessing.connection import deliver_challenge
from pydoc import describe
from statistics import mode
from telnetlib import SE
from time import timezone
from tkinter import CASCADE
from turtle import update
from venv import create
from django.db import models
from django.test import modify_settings
from matplotlib.backend_bases import MouseEvent
from sympy import N
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class Category(models.Model):
    category_name=models.CharField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    img=models.ImageField(default='default.png',upload_to='prodpics')
    def __str__(self):
        return str(self.category_name)

class Seller(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    brand=models.CharField(max_length=50)
    type=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    address=models.TextField(max_length=300,default="none")
    contact=models.IntegerField(default=0000000000,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])
    def __str__(self):
        return str(self.user.username + "-" + self.brand)

class Product(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE,null=True)
    product_name=models.CharField(max_length=50)
    prodpic=models.ImageField(default='default.png',upload_to='prodpics')
    price=models.IntegerField(default=0)
    brand=models.CharField(max_length=50,default='')
    stock=models.IntegerField(default=1000)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory=models.CharField(max_length=30,null=True,blank=True)
    desc=models.TextField(max_length=300,null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    avgrating=models.DecimalField(default=0,null=True,validators=[MinValueValidator(0),MaxValueValidator(5)],decimal_places=2,max_digits=4)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.product_name)

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return str(self.user.username+" cart")

class Orders(models.Model):
    order_code=models.CharField(default="",max_length=500)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(User, on_delete=models.CASCADE,default="")
    item=models.ForeignKey(Product, on_delete=models.CASCADE,default="")
    quantity=models.IntegerField(default=1)
    address=models.CharField(default="",max_length=500)
    city=models.CharField(default="",max_length=50)
    phone=models.CharField(default="",max_length=10)
    placed_on=models.DateTimeField(auto_now_add=True)
    delivered=models.BooleanField(default=False)
    cancelled=models.BooleanField(default=False)
    dispatched=models.BooleanField(default=False)
    def __str__(self):
        return str(str(self.customer)+str(self.order_code))

class Tracker(models.Model):
    tracking_id=models.TextField(default="")
    isdispatched=models.BooleanField(default=False)
    dispatchedtime=models.DateTimeField(auto_now_add=True)

    isreceived=models.BooleanField(default=False)
    receivedmsg=models.TextField(default="",null=True)
    receivedtime=models.DateTimeField(auto_now_add=True)

    isofd=models.BooleanField(default=False)
    ofdmsg=models.TextField(default="",null=True)
    ofdtime=models.DateTimeField(auto_now_add=True)

    isdelivered=models.BooleanField(default=False)
    deliveredtime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.tracking_id)
class Review(models.Model):
    rating=models.IntegerField(default=0,null=True,validators=[MinValueValidator(1),MaxValueValidator(5)])
    review=models.TextField(null=True,default="")
    reviewitem=models.ForeignKey(Product, on_delete=models.CASCADE,default="")
    reviewer=models.ForeignKey(User, on_delete=models.CASCADE,default="")
    added=models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.reviewitem.product_name+"-"+str(self.rating))
