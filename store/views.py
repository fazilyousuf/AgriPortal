from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Cart
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
    if checkLogin(request):
        product = Product.objects.filter(manufacturer = request.session["email"])
        user = User.objects.filter(email = request.session['email'])
        data = {'products' : product, 'user' : user[0]}
        return render(request,'farmer/home/index.html', data)
    return HttpResponse("Please Login first")

def farmer_add(request):
    user = User.objects.filter(email = request.session['email'])
    data = {'user' : user[0]}
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_image = request.FILES.get('product-image')
        product_quantity = request.POST.get('product_quantity')
        product_category = request.POST.get('category')
        product_date = request.POST.get('man-date')
        manufacturer = request.session["email"]
        new_product = Product.objects.create(name=product_name, price=product_price, image=product_image, quantity=product_quantity, category = product_category, production_date = product_date, manufacturer = manufacturer)
        new_product.save()
    if checkLogin(request):
        return render(request,'farmer/home/add_product.html',data)
    return HttpResponse("Please Login first")

def deleteitem(request, id):
    item = Product.objects.filter(id = id)
    if item:
        item.delete()
    return redirect('home_farmer')

def signup_login(request):
    return render(request,'signup_login.html')

def shop(request):
    products = Product.objects.all()
    print(type(products))
    data = {'products' : products}
    return render(request,'shop.html', data)

def addToCart(request):
    items = request.POST.getlist("items")
    for i in items:
        item, quantity = i.split(',')[0], i.split(',')[1]
        cart = Cart(user = User.objects.filter(email = request.session['email'])[0], product = Product.objects.filter(id = item)[0], quantity = int(quantity))
        cart.save()
    return HttpResponse("Cart Saved")

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
    if email == "admin@gmail.com" and passwd == "admin":
        return redirect("/admin")
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