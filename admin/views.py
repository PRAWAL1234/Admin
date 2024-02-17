from django.shortcuts import render,HttpResponse,redirect
from images.models import img
from product.models import Product,Variation
from django.core.paginator import Paginator
from django.contrib import messages,auth
from admin.form import form
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.models import cart,CartItem
from django.contrib.auth.decorators import login_required

def home(req):
    
    try:
        name=req.GET['keyword']
        product=Product.objects.filter(product_name__icontains=name)
    except:
        product=Product.objects.all()
    context={
        'product':product
    }
    return render(req,'home.html',context)

def store(req):
    try:
        name=req.GET['keyword']
        all_product=Product.objects.filter(product_name__icontains=name)
        paginator=Paginator(all_product,6)
    except:
        all_product=Product.objects.all()
        paginator=Paginator(all_product,6)


    try:
        pages=req.GET['page']
    except:
        pages=1
    all_product=paginator.get_page(pages)
    context={
        'all_product':all_product
    }
    return render(req,'store/store.html',context)

def category(req,x):
    all_product= Product.objects.filter(category__slug=x)
    context={
        'all_product':all_product
    }
    return render(req,'store/store.html',context)

def product_details(req,c_name,p_id):
    product=Product.objects.get(id=p_id)
    cat_name=Product.objects.filter(category__slug=c_name)
    color=Variation.objects.filter(product=product,variation_category="color")
    specification=Variation.objects.filter(product=product,variation_category="specification")
    context={
        'product':product,
        'category_product':cat_name,
        'color':color,
        'specification':specification
    }
    return render(req,'store/product.html',context)

@login_required(login_url='/')
def Cart(req):
    user=req.user
    cart_item=CartItem.objects.filter(user=user)
    total=0

    for i in cart_item:
        total+=i.product.price * i.quantity

    context={
        'cart_item':cart_item,
        'total':total,
        'tax':round(total*0.18,2),
        'grand_total':round(total+total*0.18,2)
    }
    return render(req,'store/cart.html',context)

def login(req):
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(req,user)
            messages.add_message(req,messages.SUCCESS,'Login Successfull')
            return redirect('/')
        else:
            messages.add_message(req,messages.ERROR,'User does not exist')
    
    return render(req,'account/login.html')

def logout(req):
    auth.logout(req)
    return redirect('/')

def signup(req):
    Form=form()
    if req.method=='POST':
        Form=form(req.POST)

        if Form.is_valid():
            first_name=req.POST['first_name']
            last_name=req.POST['last_name']
            email=req.POST['email']
            username=req.POST['username']
            password=req.POST['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password,is_active=False)
            user.save()

            Form=form()

            domain_name=get_current_site(req)
            mail_subject="Please Activate Your Account"
            userid_encode=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            message=f'http://{domain_name}/accounts/activate/{userid_encode}/{token}'
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.add_message(req,messages.SUCCESS,'Registration Success')
        else:
            messages.add_message(req,messages.ERROR,'Invaild Info')

    context={
        'form':Form
    }
    return render(req,'account/signup.html',context)

def activate(req,uid,token):
    try:
      pk= urlsafe_base64_decode(uid)
      user= User.objects.get(pk=pk)

      if default_token_generator.check_token(user,token):
         user.is_active= True
         user.save()
         messages.add_message(req,messages.SUCCESS,"Verification successful")
    except:
       messages.add_message(req,messages.ERROR,"Invalid credentials")
   
    
    return redirect('/signup')

from django.core.exceptions import ObjectDoesNotExist

def forgot(req):
    if req.method =='POST':
      email=req.POST['email']
      
      try:
         user=User.objects.get(email=email)
         domain_name= get_current_site(req)
         mail_subject= "Reset Password"
         userid_encode= urlsafe_base64_encode(force_bytes(user.pk))
         token= default_token_generator.make_token(user)
         message= f'http://{domain_name}/reset-password/{userid_encode}/{token}'
         to_email= email
       
         send_email = EmailMessage(mail_subject, message, to=[to_email])
         send_email.send()

         messages.add_message(req,messages.SUCCESS,"Reset link sent to your email")

      except ObjectDoesNotExist:
        messages.add_message(req,messages.ERROR,"No email exists")

    return render(req,'account/forgot.html')

def reset(req,uid,token):
     
    try:
        id=urlsafe_base64_decode(uid)
        user=User.objects.get(id=id)

        if default_token_generator.check_token(user,token):
            req.session['uid']=uid
            return render(req,'account/reset.html')
    except:
        redirect('/signup')

def ResetSubmit(req):
    if req.method=='POST':
        password=req.POST['password']
        confirm_password=req.POST['confirm_password']
        if password == confirm_password:

            uid=req.session['uid']
            user=User.objects.get(id=urlsafe_base64_decode(uid))

            user.set_password(password)
            user.save()

            messages.add_message(req,messages.SUCCESS,'Password Reset Successfully')
            return redirect('/login')
        else:
            messages.add_message(req,messages.ERROR,'Password are dose not match')
            return redirect('/reset-submit')
    else:
        return render(req,'account/reset.html')
    
@login_required(login_url='/')
def AddCart(req,p_id):
    product=Product.objects.get(id=p_id)
    user=req.user

    if req.method=='POST':
        color=req.POST.get('color')
        specification=req.POST.get('specification')

        color_variant=Variation.objects.get(variation_value=color,product=product)
        specification_variant=Variation.objects.get(variation_value=specification,product=product)

        current_variant=[color_variant,specification_variant]

        is_product_exists=CartItem.objects.filter(product=product,user=user).exists()

        if is_product_exists:
            l=[]
            products=CartItem.objects.filter(product=product,user=user)


            for i in products:
                l.append(list(i.variation.all()))

            if current_variant in l:
                index=l.index(current_variant)
                p=products[index]
                p.quantity+=1
                p.save()

            else:
                p=Product.objects.get(id=p_id)
                cart_item=CartItem.objects.create(product=p,user=user,quantity=1)
                cart_item.variation.add(color_variant)
                cart_item.variation.add(specification_variant)
        else:
            ci=CartItem.objects.create(product=product,user=user,quantity=1)
            ci.variation.add(color_variant)
            ci.variation.add(specification_variant)
        

    return redirect('/cart')

def remove(req,p_id):
    user=req.user
    cart_item=CartItem.objects.filter(id=p_id,user=user)
    cart_item.delete()

    return redirect('/cart')

def removeItem(req,p_id):
    user=req.user
    cart_item=CartItem.objects.get(id=p_id,user=user)

    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/cart')

def AddItem(req,p_id):
    user=req.user
    cart_item=CartItem.objects.get(id=p_id,user=user)

    try:    
        cart_item.quantity+=1
        cart_item.save()
    except:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('/cart')

import razorpay

def checkout(req):
    user=req.user
    all_product=CartItem.objects.filter(user=user)
    total=0
    for i in all_product:
        total+=i.get_total()
    client = razorpay.Client(auth=("rzp_test_IhAPDI7SHyonJY", "hfMXWN38Nj0flxUuHrcurFsl"))
    data = { "amount": total*100, "currency": "INR", "receipt": "Techshed ",'payment_capture':1}
    order=client.order.create(data)
    context={
        'item':all_product,
        'order':order
    }
    return render(req,'account/form.html',context)