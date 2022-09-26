from django.conf import settings
from django.db import models  

# Create your models here.

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
        return "%S %S" % (self.name, self.surname)

class Product(models.Model):
    name = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0.0)
    specifications = models.CharField(max_length=200, default="")
    
    def __str__(self):
        return "%S"  % (self.name)

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")


class ProductInventory(models.Model):
    in_stock = models.PositiveIntegerField(default=0)

class ProductOnQuotation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price 

class Quotation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOnQuotation)
    created_at = models.DateTimeField(auto_now_add=True) # default=timezone.now()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def total_amount(self):
        total = 0
        for quotated_product in self.products.all():
            total += quotated_product.get_total_item_price()

class PaymentMethods(models.Model):
    pass

class PaymentAmount(models.Model):
    pass

class Receipt(models.Model):
    pass

class ProductOnReceipt(models.Model):
    pass

class Discount(models.Model):
    pass

class User(models.Model):
    pass




