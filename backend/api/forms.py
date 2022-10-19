from django.forms import ModelForm
from .models import Quotation, Client

class QuotationForm(ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
