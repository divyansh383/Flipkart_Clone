from django.contrib import admin
from .models import Category, Product, Seller, Cart, Orders,Tracker, Review
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Seller)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Tracker)
admin.site.register(Review)
