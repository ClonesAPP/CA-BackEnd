from django.shortcuts import render
from django.http import HttpResponse
from .models import Quotation



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
    context = {}
    return render(request, 'api/create_quotation.html', context)