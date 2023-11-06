from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from store.models import Product
from time import time
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.

product_path = "C:/Users/ss/Desktop/agriportal/agri_p/product_image"

def checkLogin(request):
    return request.session.has_key('email')

def index(request):
    if 'email' in request.session:
        if User.objects.filter(email=request.session['email'], userType="consumer"):
            return redirect('/home_cons')
        else:
            return redirect('/home_farmer')
    else:    
        return render(request, 'index.html')


def home_cons(request):
    if checkLogin(request):
        return render(request,'home_cons.html')
    return HttpResponse("Please Login first")

def home_farmer(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_image = request.FILES.get('product-image')
        print(product_image)
        product_quantity = request.POST['product_quantity']
        product_category = request.POST['category']
        product_date = request.POST['man-date']
        new_product = Product.objects.create(name=product_name, price=product_price, image=product_image, quantity=product_quantity, category = product_category, production_date = product_date)
        new_product.save()
    if checkLogin(request):
        return render(request,'home_farmer.html')
    return HttpResponse("Please Login first")

def signup_login(request):
    return render(request,'signup_login.html')

def shop(request):
    products = Product.objects.all()
    print(products[0].image)
    data = {'products' : products}
    return render(request,'shop.html', data)

def signup(request):
    email = request.POST['email']
    usertype = request.POST['userType']
    passwd = request.POST['pswd']
    tel = request.POST['tel']
    name = request.POST['name']
    existing_user = User.objects.filter(email = email)
    if existing_user:
        return HttpResponse("User Already Exists")
    new_user = User(email=email, userType=usertype, phone=tel, name=name, passwd=passwd)
    new_user.save()
    return redirect('/signup_login')

def login(request):
    email = request.POST['loginmail']
    passwd = request.POST['loginpass']
    user = User.objects.filter(email = email)
    if user:
        if User.objects.filter(email = email, passwd = passwd):
            request.session['email'] = email
            if User.objects.filter(email = email, passwd = passwd, userType = "consumer"):
                return redirect("/home_cons")
            else:
                return redirect("/home_farmer")
        else:
            return HttpResponse("Wrong Password")
    else:
        return HttpResponse("No User Found")

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect("/")