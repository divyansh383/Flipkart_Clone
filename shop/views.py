
from ast import Delete
from gc import get_objects
from optparse import check_builtin
from select import select
from typing import ItemsView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Orders, Product, Category, Seller, Cart, Tracker, Review
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import  UserForm, NewForm, SellerForm, ProductForm
from datetime import date, datetime 
# Create your views here.
#-------------------------------
def loginpage(request):
    page="login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password) 
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Username or password does not exist")
    context={"page":page}
    return render(request,'shop/forms.html',context)
    
def logoutuser(request):
    logout(request)
    return redirect("home")

def registerpage(request):
    page="register"
    form=NewForm()
    if request.method=="POST":
        form=NewForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"error occured")

    context={"page":page,"form":form}
    return render(request,'shop/forms.html',context)


def SellerRegister(request):
    try:
        seller=Seller.objects.get(user=request.user)
        return redirect("home")
    except:
        page='sellerreg'
        form=SellerForm()
        if request.method=="POST":
            form=SellerForm(request.POST)
            if form.is_valid():
                prof=form.save(commit=False)
                prof.user=request.user
                prof.save()
                return redirect("home")
            else:
                messages.error(request,"error occured")
    context={"page":page,"form":form}
    return render(request,'shop/forms.html',context)
#------------------------------
def index(request):
    product=Product.objects.all().order_by('-created')
    user=request.user
    #cart=Cart.objects.filter(user=user)
    for i in product:
        avg=0
        num=0
        reviews=Review.objects.filter(reviewitem=i)
        for j in reviews:
            avg+=j.rating
            num+=1
        try:
            avg=avg/num
        except:
            avg=None
        i.avgrating=avg
        i.save()

    try:
        seller=Seller.objects.get(user=user)
        orders=Orders.objects.filter(seller=seller,delivered=False).count()
    except:
        seller=None
        orders=None
    category=Category.objects.all()
    
    context={"product":product,"category":category,"seller":seller,"orders":orders}
    return render(request,"shop/home.html",context)

def search(request):
    s=request.GET.get('s') 
    q=request.GET.get('q') if request.GET.get('q')!=None  else ''
    p=request.GET.get('cost') if request.GET.get('cost')!=None else 0
    isort=request.GET.get('isort')
    categories=Category.objects.all()
    

    user=request.user
    #cart=Cart.objects.filter(user=user)
    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None
    #products=Product.objects.filter(Q(category__category_name__icontains=s))
    # else:
    if s==None:
        products=Product.objects.filter(
        Q(product_name__icontains=q) |
        Q(seller__brand__icontains=q) |
        Q(subcategory__icontains=q) |
        Q(category__category_name__icontains=q)
        ).order_by("-created")
    else:
        products=Product.objects.filter(
        Q(subcategory__icontains=s) |
        Q(brand__icontains=s) &
        Q(price__lte=p)).order_by(isort)

    context={"product":products,"category":categories,"seller":seller,"p":p,"q":q,"s":s}
    return render(request,"shop/search.html",context)

def cart(request):
    user=User.objects.get(username=request.user)

    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    prev=Cart.objects.filter(user=user)
    subtotal=0
    itemcount=0
    for i in prev:
        subtotal+=i.product.price*i.quantity
        itemcount+=i.quantity
    
    items=Cart.objects.all()
    product=Product.objects.all()
    context={"user":user,"items":items,"product":product,"seller":seller,"subtotal":subtotal,"itemcount":itemcount}
    return render(request,"shop/cart.html",context)
    
def productView(request,pk):
    product=Product.objects.get(id=pk)
    reviews=Review.objects.filter(reviewitem=product).order_by('added')
    try:
        rev=request.POST.get('rev')
        q=request.POST.get('q')
    except:
        rev=None
    if rev!=None:
        writerev=Review()
        writerev.rating=q
        writerev.review=rev
        writerev.reviewitem=product
        writerev.reviewer=request.user
        writerev.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    try:
        seller=Seller.objects.get(user=request.user)
    except:
        seller=None
    avg=0
    num=0
    for j in reviews:
        avg+=j.rating
        num+=1
    try:
        avg=avg/num
    except:
        avg=None
    
    product.avgrating=avg
    product.save()
    
    context={"product":product,"seller":seller,"reviews":reviews}
    return render(request,"shop/product-view.html",context)

@login_required(login_url="login-page")
def addproduct(request):
    try:
        seller=Seller.objects.get(user=request.user)
    except:
        seller=None
    form=ProductForm()
    page="addproduct"
    if seller.user==request.user:
        if request.method =="POST":
            form=ProductForm(request.POST,request.FILES)
            if form.is_valid():
                prod=form.save(commit=False)
                prod.seller=seller
                prod.save()
                return redirect("home")
                
        context={'form':form,"page":page}
        return render(request,"shop/forms.html",context)
    else: 
        return redirect("home")


@login_required(login_url="login-page")
def addtocart(request):
    user=User.objects.get(username=request.user)
    prev=Cart.objects.filter(user=user)
    previtems=[]
    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    for i in prev:
        previtems.append(i.product)
    if user==request.user:
        if request.method =="GET":
            if user.is_authenticated:
                pr=request.GET.get('product')
                product=Product.objects.get(product_name=pr)
                item=Cart(user=user,product=product)
                if item.product not in previtems:
                    item.save()
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    chitem=Cart.objects.get(user=user,product=product)
                    chitem.quantity+=1
                    chitem.save()
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                page="login"
                context={"page":page}
                return render(request,'shop/forms.html',context)

    context={"user":user,"seller":seller}
    return render(request,"shop/search.html",context)

def removeitem(request):
    user=User.objects.get(username=request.user)
    minus=request.GET.get("-")
    if user==request.user:
        if request.method =="GET":
            if  minus==None:
                pid=request.GET.get('pid')            
                item=Cart.objects.get(id=pid)
                item.delete()
                return redirect("cart")
            else:
                pid=request.GET.get('pid')    
                chitem=Cart.objects.get(id=pid)
                chitem.quantity-=1
                if chitem.quantity==0:
                    chitem.delete()
                else:
                    chitem.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))

    context={"user":user}
    return render(request,"shop/search.html",context)


@login_required(login_url="login-page")
def placeorder(request):
    today=date.today()
    now=datetime.now()
    tim=now.strftime("%Y-%m-%d %H:%M")
    tc=str(now.strftime("%y%m%d%H%M%S"))
    user=request.user
    address=request.GET.get('address')
    city=request.GET.get('city')
    phone=request.GET.get('phone')
    crtitems=Cart.objects.filter(user=user)
    code=str(request.user.id)+str(phone[7:])+tc
    ordlist=[]
    for items in crtitems:
        ords=Orders()
        ords.order_code=code
        ords.seller=items.product.seller
        ords.customer=user
        ords.item=items.product
        ords.quantity=items.quantity
        ords.address=address
        ords.city=city
        ords.phone=phone
        ords.placed_on=tim
        ordlist.append(ords)

    Orders.objects.bulk_create(ordlist)
    trk=Tracker(tracking_id=code)
    trk.save()
    return redirect('yourorder')

def yourorder(request):
    user=User.objects.get(username=request.user)

    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    orders=Orders.objects.filter(customer=user).order_by("-placed_on")
   
    context={"user":user,"orders":orders,"seller":seller}
    #return HttpResponse("orders")
    return render(request,"shop/orders.html",context)

@login_required(login_url="login-page")
def deals(request):
    updates=request.POST.getlist("check")
    user=User.objects.get(username=request.user)
    
    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    orders=Orders.objects.filter(seller=seller)
    for x in updates:
        for i in orders:
            if(int(i.order_code)==int(x)):
                i.dispatched=True
                prods=Product.objects.get(product_name=i.item.product_name)
                prods.stock-=int(i.quantity)
                prods.save()
                i.save()

    context={"user":user,"orders":orders,"seller":seller,"updates":updates}
    #return HttpResponse("orders")
    return render(request,"shop/deals.html",context)

def cancelorder(request,tid):
    ords=Orders.objects.filter(order_code=tid)
    for i in ords:
        i.cancelled=True
        prods=Product.objects.get(product_name=i.item.product_name)
        prods.stock+=int(i.quantity)
        prods.save()
        i.save()
    return redirect('yourorder')

@login_required(login_url="login-page")
def updatetracker(request,tid):
    user=User.objects.get(username=request.user)
    stts=request.POST.get('status')
    dets=request.POST.get('msge')
    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    order=Orders.objects.filter(order_code=tid)
    trk=Tracker.objects.get(tracking_id=tid)
    disp=True
    for i in order:
        if(not i.dispatched):
            disp=False
            break
    #---------------------------------
    if disp and trk.isdispatched==False:
        trk=Tracker.objects.get(tracking_id=tid)
        now=datetime.now()
        tim=now.strftime("%Y-%m-%d %H:%M")
        trk.isdispatched=True
        trk.dispatchedtime=tim
        trk.save()
    #----------------
    if(stts=="recieved"):
        print("----------recieved-------------")
        trk=Tracker.objects.get(tracking_id=tid)
        trk.isreceived=True
        now=datetime.now()
        tim=now.strftime("%Y-%m-%d %H:%M")
        trk.receivedtime=tim
        trk.receivedmsg=dets
        trk.save()
    #-------------------------
    if(stts=="out_for_delivery"):
        print("-----------------------")
        trk=Tracker.objects.get(tracking_id=tid)
        trk.isofd=True
        now=datetime.now()
        tim=now.strftime("%Y-%m-%d %H:%M")
        trk.ofdtime=tim
        trk.ofdmsg=dets
        trk.save()
        
    #--------------------
    if(stts=="delivered"):
        trk=Tracker.objects.get(tracking_id=tid)
        trk.isdelivered=True
        now=datetime.now()
        tim=now.strftime("%Y-%m-%d %H:%M")
        trk.deliveredtime=tim
        trk.save()
        return redirect('all_orders')
    #-------------------------
    context={"user":user,"order":order,"tracker":trk,"seller":seller,"stts":stts,"dets":dets}
    return render(request,"shop/updatetracker.html",context)


def tracker(request,tid):
    user=User.objects.get(username=request.user)

    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None
    tracker=Tracker.objects.get(tracking_id=tid)
    order=Orders.objects.filter(order_code=tid)
    context={"user":user,"order":order,"tid":tid,"seller":seller,"tracker":tracker}
    return render(request,"shop/trackingpage.html",context)

@login_required(login_url="login-page")
def manageorders(request):
    user=User.objects.get(username=request.user)

    try:
        seller=Seller.objects.get(user=user)
    except:
        seller=None

    orders=Orders.objects.all()
    tracker=Tracker.objects.filter(isdelivered=True)
    for i in tracker:
        for p in orders:
            if(int(p.order_code)==int(i.tracking_id)):
                if(not p.delivered):
                    p.delivered=True
                    p.save()

    context={"user":user,"orders":orders,"seller":seller}
    #return HttpResponse("orders")
    return render(request,"shop/allords.html",context)
