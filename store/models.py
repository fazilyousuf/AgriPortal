from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    passwd = models.CharField(max_length=26, null=True)
    userType = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    address = models.TextField(null=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=20, null=True)
    quantity = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=15, null=True)
    production_date = models.CharField(max_length=15, null=True)
    image = models.ImageField(upload_to ='media/')
    manufacturer = models.CharField(max_length=30, null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totalamount = models.IntegerField(default=0)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created"]

class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    packed = models.BooleanField(default=False)

    class Meta:
        ordering = ["packed","order"]