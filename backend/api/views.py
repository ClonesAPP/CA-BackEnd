from tkinter.font import ROMAN
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quotation
from .forms import QuotationForm    


# Create your views here.
def home(request):
    quotations = Quotation.objects.all()
    context = {'quotations': quotations}
    return render(request, 'api/home.html', context)

def quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    context = {'quotation': quotation}
    return render(request, 'api/quotation.html', context)

def create_quotation(request):
    form = QuotationForm()
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
            
    context = {'form': form}
    return render(request, 'api/create_quotation.html', context)

