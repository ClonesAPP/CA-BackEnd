from django.forms import ModelForm
from .models import Quotation, Client, ProductOnQuotation, Product, ProductCategory, Discount, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    identification = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "identification",
            "email",
            "password1",
            "password2"
            )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.identification = self.cleaned_data['identification']
        if commit:
            user.save()
        print(user)
        return user

class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class QuotationForm(ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

class ProductOnQuotationForm(ModelForm):
    class Meta:
        model = ProductOnQuotation
        fields = '__all__'

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ("identification",)