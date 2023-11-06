from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    passwd = models.CharField(max_length=26, null=True)
    userType = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=20, null=True)
    quantity = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=15, null=True)
    production_date = models.CharField(max_length=15, null=True)
    image = models.ImageField(upload_to ='media/')
    manufacturer = models.CharField(max_length=30, null=True)