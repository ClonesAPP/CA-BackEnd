
from email import message
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from backend.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .models import Quotation, ProductOnQuotation, Product
from .forms import ClientForm, QuotationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, ("Datos incorrectos, vuelva a intentar"))
            return redirect("login")
    else:
        return render(request, 'registration/login.html', {})

@login_required(redirect_field_name="login")
def logout_user(request):
    logout(request)
    return redirect("login")

@login_required(redirect_field_name="login")
def home(request):
    return render(request, 'home.html')

@login_required(redirect_field_name="login")
def see_quotations(request):
    quotations = Quotation.objects.all()
    context = {'quotations': quotations}
    return render(request, 'quotations.html', context)

@login_required(redirect_field_name="login")
def quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    context = {'quotation': quotation}
    return render(request, 'quotation.html', context)

@login_required(redirect_field_name="login")
def create_quotation(request):
    form = QuotationForm()
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
            
    context = {'form': form}
    return render(request, 'create_quotation.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_client(request):
    form = ClientForm()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'create_client.html', context)
