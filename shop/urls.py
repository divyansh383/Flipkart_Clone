from django.urls import path
from .import views
urlpatterns = [
    path("login/",views.loginpage,name="login-page"),
    path("logout/",views.logoutuser,name="logout"),
    path("register/",views.registerpage,name="register"),
    path("seller-register/",views.SellerRegister,name="selreg"),

    path('',views.index,name="home"),
    path('search/', views.search ,name="search"),
    path('cart/',views.cart,name='cart'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('yourorder/',views.yourorder,name='yourorder'),
    path('deals/',views.deals,name='deals'),
    path("manageorders/",views.manageorders, name="all_orders"),
    
    path('tracker/<str:tid>', views.tracker,name="TrackingStatus"),
    path('updatetracker/<str:tid>', views.updatetracker,name="updatetracker"),
    path('productview/<str:pk>', views.productView,name="productview"),
    path('add-product/', views.addproduct,name="add-product"),
    path('add-to-cart/',views.addtocart,name='addtocart'),
    path('removeitem/',views.removeitem,name='removeitem'),
    path('cancelorder/<str:tid>',views.cancelorder,name='cancelorder')
    
]