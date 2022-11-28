from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# Register your models here.

from .models import *

class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False

class AccountUserAdmin(AuthUserAdmin):
    inlines = [UserProfileInLine]

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
admin.site.unregister(User)
admin.site.register(User, AccountUserAdmin)
