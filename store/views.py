from django.shortcuts import render,redirect,HttpResponse
from store.models import *
from store.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import razorpay

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


# Create your views here.
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1==pass2:
            customer=User.objects.create_user(username,email,pass1)
            customer.first_name=first_name
            customer.last_name=last_name
            customer.save()
            return redirect('/login')
        else:
            msg="*The password confirmation does not match"
            res= render(request,'store/signup.html',{'msg':msg})
        return res
    
    res= render(request,'store/signup.html')
    return res

def HandleLogin(request):
    if request.method=='POST':
        cart=request.session.get('cart')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            #cart={}
            request.session['cart']=cart
            request.session['user']=username
            return redirect('/')
        else:
            return redirect('/login')

    res= render(request,'store/login.html')
    return res

def HandleLogout(request):
    logout(request)
    return redirect('/login')

def about(request):
    res= render(request,'store/about.html')
    return res

def Search(request):
    query=request.GET.get('query')
    product=Product.objects.filter(name__icontains=query)
    res=render(request,'store/search.html',{'product':product})
    return res

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        contact=Contact_us(
            Name=name,
            email=email,
            subject=subject,
            message=message,
        )
        if name=='' or email=='' or subject=='' or message=='':
            msg="* Please fill all the fields."
            res= render(request,'store/contact.html',{'msg':msg})
            return res
        else:
            contact.save()
            return redirect('/index')

    res= render(request,'store/contact.html')
    return res

def Product_Details(request):
    if request.method=='GET':
        product_id=request.GET.get('product_id')
        product=Product.objects.filter(id=product_id)
        res=render(request,'store/single_product.html',{'product':product})
        return res
    else:
        product_id=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product_id)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product_id)
                    else:
                        cart[product_id]=quantity-1
                else:
                    cart[product_id]=quantity+1
            else:
                cart[product_id]=1
        else:
            cart={}
            cart[product_id]=1
        
        request.session['cart']=cart
        # print('Cart',request.session['cart'])
        product=Product.objects.filter(id=product_id)
        res=render(request,'store/single_product.html',{'product':product})
        return res

def index(request):
    cart=request.session.get('cart')
    if cart:
        pass
    else:
        cart={}
        request.session['cart']=cart
    brand=Brand.objects.all()
    filter_price=Filter_Price.objects.all()
    category=Categories.objects.all()

    category_id=request.GET.get('category_id')
    price_filter_id=request.GET.get('price_filter')
    brand_id=request.GET.get('brand_id')

    cat1=request.GET.get('cat1')
    if cat1:
        catt1=Categories.objects.filter(name='Mobiles & Accessories')
        for x in catt1:
            cat_id=x.id
    
    cat2=request.GET.get('cat2')
    if cat2:
        catt2=Categories.objects.filter(name='Laptop & Accessories')
        for x in catt2:
            cat_id=x.id

    cat3=request.GET.get('cat3')
    if cat3:
        catt3=Categories.objects.filter(name='Electronics')
        for x in catt3:
            cat_id=x.id
    
    
    
    ATOZ=request.GET.get('ATOZ')
    ZTOA=request.GET.get('ZTOA')
    LTH=request.GET.get('LTH')
    HTL=request.GET.get('HTL')
    cnd=request.GET.get('cnd')

    if cat1 or cat3:
        product=Product.objects.filter(category=cat_id,status='Publish')
    elif cat2:
        product=Product.objects.filter(category=cat_id,status='Publish')
    elif category_id:
        product=Product.objects.filter(category=category_id,status='Publish')
    elif price_filter_id:
        product=Product.objects.filter(filter_price=price_filter_id,status='Publish')
    elif brand_id:
        product=Product.objects.filter(brand=brand_id,status='Publish')
    elif ATOZ:
        product=Product.objects.filter(status='Publish').order_by('name')
    elif ZTOA:
        product=Product.objects.filter(status='Publish').order_by('-name')
    elif LTH:
        product=Product.objects.filter(status='Publish').order_by('price')
    elif HTL:
        product=Product.objects.filter(status='Publish').order_by('-price')
    elif cnd:
        product=Product.objects.filter(condition=cnd,status='Publish')
    else:
        product=Product.objects.filter(status='Publish')

    content={
            'product':product,
            'category':category,
            'filter_price':filter_price,
            'brand':brand,
        }
    res= render(request,'store/index.html',content)
    return res

@login_required(login_url="/login")
def Cart(request):
    if request.method=='GET':
        cart=request.session.get('cart')
        if cart:
            pass
        else:
            cart={}
            request.session['cart']=cart
        ids=list(cart.keys())
        product=Product.objects.filter(id__in=ids)
        res=render(request,'store/cart.html',{'product':product})
        return res
    
    else:
        product_id=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        quantity=cart.get(product_id)
        
        if remove:
                    if quantity==1:
                        cart.pop(product_id)
                    else:
                        cart[product_id]=quantity-1
        else:
                    cart[product_id]=quantity+1
        
        request.session['cart']=cart
        ids=list(request.session.get('cart').keys())
        product=Product.objects.filter(id__in=ids)
        res=render(request,'store/cart.html',{'product':product})
        return res

def CheckOut(request):
    amount=int(request.POST.get('amount'))
    amount=amount*100
    ids=list(request.session.get('cart').keys())
    product=Product.objects.filter(id__in=ids)
    payment= client.order.create({
        "amount":amount,
        "currency":"INR",
        "payment_capture":"1"
    })
    
    order_id=payment['id']
    context={
        'order_id':order_id,
        'payment':payment,
        'product':product,
    }

    return render(request,'store/checkout.html',context)

def PlaceOrder(request):
    if request.method=='POST':
        ids=list(request.session.get('cart').keys())
        product=Product.objects.filter(id__in=ids)
        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(id=uid)
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        country=request.POST.get('country')
        address=request.POST.get('address')
        state=request.POST.get('state')
        city=request.POST.get('city')
        postcode=request.POST.get('postcode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        amount=request.POST.get('amount')

        cart=request.session.get('cart')
        
        context={
            'order_id':order_id,
            'product':product,
        }

        order=Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            state=state,
            city=city,
            postcode=postcode,
            phone=phone,
            email=email,
            payment_id=order_id,
            amount=amount,
        )
        order.save()

        for i in ids:
            p=Product.objects.filter(id=i)
            for z in p:
                name=z.name
                image=z.image
                price=z.price
                quantity=cart[i]
                total=int(quantity)*int(price)
                item=OrderItems(
                    order=order,
                    product=name,
                    image=image,
                    quantity=quantity,
                    price=price,
                    total=total,
                )
                item.save()
        res=render(request,'store/placeorder.html',context)
        return res
@csrf_exempt  
def success(request):
    if request.method=="POST":
        a=request.POST
        order_id=""
        for key, val in a.items():
            if key=='razorpay_order_id':
                order_id=val
                break
        user=Order.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
    return render(request,'store/thank-you.html')

def LandingPage(request):
    return render(request,'store/landing-page.html')
    