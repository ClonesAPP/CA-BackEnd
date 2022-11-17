
from email import message
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from backend.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .models import Quotation, ProductOnQuotation, Product, Client
from .forms import ClientForm, QuotationForm, ProductOnQuotationForm, ProductForm, ProductCategoryForm, DiscountForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction


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

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def see_clients(request):
    clients = Client.objects.all()
    context = {'clients': clients}

    return render(request, 'view_users.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def update_client(request, client_id):
    try: 
        client_to_update = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect('home')

    client_form = ClientForm(request.POST or None, instance=client_to_update)
    if client_form.is_valid():
        client_form.save()
        return redirect('home')
    context = {'client': client_form}
    print(context)
    return render(request, 'update_user.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def delete_client(request, client_id):
    try:
        client_to_delete = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect('home')
    client_to_delete.delete()
    return redirect('home')

@login_required(redirect_field_name="login")
def quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    context = {'quotation': quotation}
    return render(request, 'quotation.html', context)

@login_required(redirect_field_name="login")
def create_quotation(request):
    form = QuotationForm()
    form2 = ProductOnQuotationForm()
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
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'create_client.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create_product.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_category(request):
    form = ProductCategoryForm()

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create_category.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def create_discount(request):
    form = DiscountForm()

    if request.method == 'POST':
        form = DiscountForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'create_discount.html', context)


@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def see_products(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'see_products.html', context)

@login_required(redirect_field_name="login")
def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'product.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def update_product(request, product_id):
    try: 
        product_to_update = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('home')

    product_form = ProductForm(request.POST or None, instance=product_to_update)
    if product_form.is_valid():
        product_form.save()
        return redirect('home')
    context = {'product': product_form}
    return render(request, 'update_product.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def delete_product(request, product_id):
    try:
        product_to_update = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('home')
    product_to_update.delete()
    return redirect('home')

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
@transaction.atomic
def update_profile(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_prof_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and user_prof_form.is_valid():
            user_form.save()
            user_prof_form.save()   
            return redirect("user:profile")
    else:
        user_form = UserForm(instance=request.user)
        user_prof_form = UserProfileForm(instance=request.user.userprofile)
    
    context = {'user_form':user_form, 'up_form':user_prof_form}
    return render(request, 'profile.html', context)
