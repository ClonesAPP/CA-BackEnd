from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Client)
admin.site.register(ProductCategory)
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(ProductInventory)
admin.site.register(ProductOnQuotation)
admin.site.register(Quotation)
admin.site.register(PaymentMethods)
admin.site.register(Payment)
admin.site.register(Receipt)
admin.site.register(ProductOnReceipt)
