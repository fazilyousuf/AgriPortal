from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Cart, Order, OrderItems
from store.models import Product
from time import time
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Count, Q
from datetime import date, timedelta

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
def deleteitemAdmin(request, id):
    item = Product.objects.filter(id = id)
    if item:
        item.delete()
    return redirect('home_admin')

def signup_login(request):
    return render(request,'signup_login.html')

def shop(request):
    q = request.GET.get("q")
    category = request.GET.get("category")
    print(category)
    if category != None:
        products = Product.objects.filter(category = category)
    else:
        if q == None:
            q = ''
        products = Product.objects.filter(name__icontains = q)
    categories = Product.objects.all().values("category").annotate(total = Count("category"))
    total = Product.objects.all().count
    data = {'products' : products, 'categories' :categories, 'total' : total}
    return render(request,'shop.html', data)

def addToCart(request):
    items = request.POST.getlist("items")
    for i in items:
        item, itemquantity = i.split(',')[0], i.split(',')[1]
        obj = Cart.objects.filter(user = User.objects.filter(email = request.session['email'])[0], product = Product.objects.filter(id = item)[0])
        if obj.exists():
            print()
            new_obj = obj[0]
            qnty = new_obj.quantity
            new_obj.quantity = qnty+int(itemquantity)
            new_obj.save()
        else:
            cart = Cart(user = User.objects.filter(email = request.session['email'])[0], product = Product.objects.filter(id = item)[0], quantity = int(itemquantity))
            cart.save()
    return redirect('/cart')

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
        request.session['email'] = email
        return redirect("home_admin")
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

def viewCart(request):
    user = User.objects.filter(email = request.session['email'])[0]
    cart_item = Cart.objects.filter(user = user)
    total = 0
    for i in cart_item:
        total += i.quantity * int(i.product.price)
    items = {"items" : cart_item, 'total' : total, 'user' : user}
    return render(request, 'consumer/cart.html', items)

def updatecart(request):
    products = request.POST.getlist("product")
    count = request.POST.getlist("count")
    user = User.objects.get(email = request.session['email'])
    print(products)
    for i, j in enumerate(products):
        product = Product.objects.get(id=j)
        cart = Cart.objects.get(Q(user=user) & Q(product = product))
        cart.quantity = count[i]
        cart.save()
    return redirect('cart')

def removeItem(request):
    item = request.GET.get('item')
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(id=item)
    cart = Cart.objects.get(Q(user=user) & Q(product = product))
    cart.delete()
    return redirect('cart')

def placeOrder(request):
    user = User.objects.get(email = request.session['email'])
    products = {}
    items = Cart.objects.filter(user = user)
    total = 0
    newOrder = Order(user = user)
    newOrder.save()
    for i in items:
        product = i.product
        quantity = i.quantity
        amount = i.product.price
        orderitem = OrderItems(product = product, quantity=quantity, amount=amount, order = newOrder)
        orderitem.save()
        total+=i.quantity*int(i.product.price)
    newOrder.totalamount = total
    newOrder.save()
    items.delete()
    return redirect('shop')

def changeFarmerPassword(request):
    user = User.objects.get(email = request.session['email'])
    data = {'user' : user}
    if request.method == 'POST':
        user.passwd = request.POST.get("password")
        user.save()
    return render(request, 'farmer/home/changePassword.html', data)

def viewOrders(request):
    user = User.objects.get(email = request.session['email'])
    orders = OrderItems.objects.filter(product__manufacturer = request.session['email'])
    data = {'user' : user, 'orders' : orders}
    print(orders)
    return render(request, 'farmer/home/orders.html', data)

def orderSended(request):
    order = request.GET.get('orderid')
    orderObject = OrderItems.objects.get(id=order)
    orderObject.packed = True
    orderObject.save()
    return redirect('view-orders')

def statistics(request):
    user = User.objects.get(email = request.session['email'])
    # today = date.today()
    today = OrderItems.objects.filter(product__manufacturer = request.session['email'], order__created = date.today())
    print(today)
    amt = 0
    for i in today:
        amt+=i.amount
    todayData = {'orders' : today.count, 'amount' : amt}
    amt = 0
    start = date.today().replace(day=1)
    month = OrderItems.objects.filter(product__manufacturer = request.session['email'],order__created__gte = start, order__created__lte = date.today())
    # print(month)
    for i in month:
        amt+=i.amount
    monthData = {'orders' : month.count, 'amount' : amt}
    amt = 0
    start = date.today() - timedelta(days=7)
    week = OrderItems.objects.filter(product__manufacturer = request.session['email'],order__created__gte = start, order__created__lte = date.today())
    for i in week:
        amt+=i.amount
    weekData = {'orders' : week.count, 'amount' : amt}
    data = {'user' : user, 'today' : todayData, 'month' : monthData, 'week' : weekData}
    return render(request, 'farmer/home/statistics.html', data)

def consumerOrders(request):
    orders = Order.objects.filter(user = request.session['email'])
    data = {'orders' : orders, 'day' : date.today() - timedelta(days=1)}
    return render(request, 'consumer/view-orders.html', data)

def cancelConsumerOrder(request):
    id = request.GET.get("id")
    order = Order.objects.get(id = id)
    order.delete()
    return redirect('/consumer-orders')

def profile(request):
    data ={}
    return render(request, 'consumer/my-account.html', data)

def address(request):
    user = User.objects.get(email = request.session['email'])
    data = {'present' : user.address}
    if request.method == 'POST':
        address = request.POST.get('address')
        if len(address) < 20:
            data['warning'] = "Please Write a Address More Specific"
            return render(request, 'consumer/address.html', data)
        user.address = address
        user.save()
        return('home_cons')
    return render(request, 'consumer/address.html', data)

def editCredentials(request):
    user = User.objects.get(email = request.session['email'])
    data = {'user' : user}
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user.name = name
        user.phone = phone
        user.passwd = password
        user.save()
        return redirect('/profile')
    return render(request, 'consumer/edit-credentials.html', data)

def editProduct(request):
    id = request.GET.get("id")
    product = Product.objects.get(id = id)
    data = {'product' : product}
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_image = request.FILES.get('product-image')
        product_category = request.POST.get('category')
        product_date = request.POST.get('man-date')
        product.name = product_name
        product.price = product_price
        if product_image != None:
            product.image = product_image
        product.category = product_category
        product.production_date = product_date
        product.save()
        return redirect('home_farmer')
    return render(request, 'farmer/home/edit_product.html', data)

def adminIndex(request):
    products = Product.objects.all()
    data = {"products" : products}
    return render(request, 'admin/index.html', data)