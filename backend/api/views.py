from django.shortcuts import render
from django.http import HttpResponse

quotations = [
    {'id': 1, 'nombre': 'kms'},
    {'id': 2, 'nombre': 'kms'},
    {'id': 3, 'nombre': 'kms'}
]

# Create your views here.
def home(request):
    return render(request, 'api/home.html')

def quotation(request, pk):
    quotation = None

    for i in quotations
    
    return render(request, 'api/quotation.html')

def create_quotation(request):
    context = {}
    return render(request, 'api/quotation.html', context)