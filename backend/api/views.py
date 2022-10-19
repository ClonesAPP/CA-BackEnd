
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from backend.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .models import Quotation, ProductOnQuotation, Product
from .forms import ClientForm, QuotationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def home(request):
    quotations = Quotation.objects.all()
    context = {'quotations': quotations}
    return render(request, 'api/home.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    context = {'quotation': quotation}
    return render(request, 'api/quotation.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_quotation(request):
    form = QuotationForm()
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
            
    context = {'form': form}
    return render(request, 'api/create_quotation.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_client(request):
    form = ClientForm()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'api/create_client.html', context)
