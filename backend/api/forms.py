from django.forms import ModelForm
from .models import Quotation, Client, ProductOnQuotation, Product, ProductCategory, Discount

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

