from pyexpat import model
from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    identification = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100, default="")
    # user_type_choices = models.TextChoices('user_type', 'admin staff'),
    # user_type = models.CharField(blank=True, choices=user_type_choices.choices, max_length=10),
    phone = models.CharField(max_length=15)
    cell_number = models.CharField(max_length=15, default="")
    city = models.CharField(max_length=60),  # CHANGE THIS TO OPTIONS  USING DJANGO-CITIES FOR LATER SPRINTS

    def __str__(self):
        return "%S %S" % (self.name, self.surname)

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    specifications = models.CharField(max_length=200)
    
    def __str__(self):
        return "%S"  % (self.name)

class PaymentMethods(models.Model):
    pass

class ProductCategory(models.Model):
    pass

class ProductInventory(models.Model):
    pass