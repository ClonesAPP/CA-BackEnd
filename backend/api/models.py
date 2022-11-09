from secrets import choice
from tkinter import CASCADE
from typing import Dict
from django.conf import settings
from django.db import models  

# Create your models here.
PAYMENT_OPTIONS = (
    ('C', 'Cash'),
    ('CC', 'Credit Card'),
    ('OT', 'Other'),
)

class Client(models.Model):
    name = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50, default="")
    email = models.EmailField(unique=True, default="")
    identification = models.CharField(max_length=50, unique=True, default="")
    address = models.CharField(max_length=100, default="")
    # user_type_choices = models.TextChoices('user_type', 'admin staff'),
    # user_type = models.CharField(blank=True, choices=user_type_choices.choices, max_length=10),
    phone = models.CharField(max_length=15, default="")
    cell_number = models.CharField(max_length=15, default="")
    city = models.CharField(max_length=60, default="")  # CHANGE THIS TO OPTIONS  USING DJANGO-CITIES FOR LATER SPRINTS

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")

    def __str__(self):
        return "%s" % (self.name)

class Discount(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")
    discount_percentage = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, default=True, null=False)
    name = models.CharField(max_length=50,  default="", null=False)
    price = models.DecimalField(max_digits=15, decimal_places=0,  default=True, null=False)
    specifications = models.CharField(max_length=200,  default="", null=False)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.name)

    def get_discount_price(self):
        return self.price * self.discount.discount_percentage

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True, null=False)
    quantity = models.PositiveIntegerField(default=0)

class ProductOnQuotation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.product.get_discount_price

    def get_total_price(self):
        if self.product.discount.active:
            return self.get_total_item_price()
        return self.get_total_discount_item_price()

class Quotation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOnQuotation)
    created_at = models.DateTimeField(auto_now_add=True) # default=timezone.now()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.client.name
    
    def get_total_amount(self):
        total = 0
        for quotated_product in self.products.all():
            total += quotated_product.get_total_item_price()
        return total

class PaymentMethods(models.Model):
    payment_method = models.CharField(choices=PAYMENT_OPTIONS, max_length=12)
    charge_percentage = models.FloatField(default=1.0)

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.client.name

class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOnQuotation)
    created_at = models.DateTimeField(auto_now_add=True) # default=timezone.now()
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.cliente.name
    
    def get_total_amount(self):
        total = 0
        for quotated_product in self.products.all():
            total += quotated_product.get_total_item_price()

class ProductOnReceipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.product.get_discount_price

    def get_total_price(self):
        if self.product.discount.active:
            return self.get_total_item_price()
        return self.get_total_discount_item_price()






