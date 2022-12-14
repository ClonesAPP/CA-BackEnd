
from email import message
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from backend.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .models import Quotation, ProductOnQuotation, Product, Client, UserProfile, ProductCategory
from .forms import ClientForm, QuotationForm, ProductOnQuotationForm, ProductForm, ProductCategoryForm, DiscountForm, UserForm, UserProfileForm, NewUserForm
from .forms import PaymentForm, ReceiptForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
import json
from .utils import quotationData
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save()

            if 'quotationid' in request.session:
                del request.session['quotationid']

            request.session['quotationid'] = quotation.pk

            return redirect('add-products')
            
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

@login_required(redirect_field_name="login")
def client(request, pk):
    client = Client.objects.get(id=pk)
    context = {'client': client}
    return render(request, 'client.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def see_products(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {'products': products, 'categories': categories}

    return render(request, 'see_products.html', context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def see_products_category(request, cats):
    category = ProductCategory.objects.get(id=cats)
    products = Product.objects.filter(category=category)
    context = {'products': products}

    return render(request, 'see_products.html', context)


@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def add_products(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'add_products.html', context)

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
            return redirect("profile")
    else:
        user_form = UserForm(instance=request.user)
        user_prof_form = UserProfileForm(instance=request.user.userprofile)
    
    context = {'user_form':user_form, 'up_form':user_prof_form}
    return render(request, 'profile.html', context)

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            identification = form.cleaned_data.get('identification')
            
            UserProfile.objects.filter(user_id = user.id).update(identification = identification)
            login(request, user)
            messages.success(request, "Se ha registrado correctamente.")
            return redirect('home')

        password1 = form.data['password1']
        password2 = form.data['password2']
        for msg in form.errors.as_data():
            if msg == 'email':
                messages.error(request, f"El email ingresado no es valido.")
            if msg == 'password2' and password1 == password2:
                messages.error(request, f"La contrase??a no es lo suficientemente fuerte.")
            elif msg == 'password2' and password1 != password2:
                messages.error(request, f"Las contrase??as ingresadas no coinciden.")

        messages.error(request, "El nombre de usuario ya existe, intente con otro.")

    form = NewUserForm()
    context = {'register_form':form}
    
    return render(request, 'registration.html', context)

def about_us(request):
    return render(request, 'about_us.html')

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def update_quotation(request):
    data = json.loads(request.body)
    productId = data['productId']
    quotationId = data['quotationId']
    action = data['action']

    print('Action', action)
    print(productId)
    print('QuotationId:', quotationId)

    product = Product.objects.get(id=productId)
    quotation = Quotation.objects.get(id=quotationId)
    user = quotation.user

    productOnQuotation, created = ProductOnQuotation.objects.get_or_create(user=user, quotation=quotation, product=product)
    print(productOnQuotation)
    if action == "add":
        productOnQuotation.quantity = (productOnQuotation.quantity + 1)
    elif action == "remove":
        productOnQuotation.quantity = (productOnQuotation.quantity - 1)

    productOnQuotation.save()

    if productOnQuotation.quantity <= 0:
        productOnQuotation.delete()

    return JsonResponse('Producto agregado con exito', safe=False)

def delete_quotation(request, quotation_id):
    try:
        quotation_to_delete = Quotation.objects.get(id=quotation_id)
    except Quotation.DoesNotExist():
        return redirect('home')
    quotation_to_delete.delete()
    return redirect('see-quotations')


def cart(request, quotation_id):
    data = quotationData(request, quotation_id)
    print(data)
    quotation_items = data['quotation_items']
    quotation = data['quotation']
    items = data['items']

    context = {'items':items, 'quotation':quotation, 'quotation_items':quotation_items}
    
    return render(request, 'cart.html', context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Solicitud de Cambio de Contrase??a"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Octocon',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'un.otocon@gmail.com', [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'Se ha enviado un mensaje a su correo con las instrucciones para resetear la contrase??a.')
					return redirect ("home")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

def CategoryView(request, cats):
    category = Product.objects.filter(category=cats.replace('-', ' '))
    context = {'cats': cats.replace('-', ' ').title(), 'category_posts': category}
    return render(request, "categories.html", context)

@login_required(redirect_field_name=LOGOUT_REDIRECT_URL)
def search_quotation(request):
    context = {}
    if request.method == 'POST':
        searched = request.POST['searched']
        quotation = Quotation.objects.filter(client__contains=searched)

        context = {'searche':searched,'quotation': quotation}
        return render(request, 'search_quotation.html', context)
    else:
        return render(request, 'search_quotation.html', context)


@login_required(redirect_field_name="login")
def create_recepit(request):
    form = ReceiptForm()
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()

            return redirect('home')

@login_required(redirect_field_name="login")
def create_quotation(request):
    form = QuotationForm()
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save()

            if 'quotationid' in request.session:
                del request.session['quotationid']

            request.session['quotationid'] = quotation.pk

            return redirect('add-products')
            
    context = {'form': form}
    return render(request, 'create_quotation.html', context)


def analytics(request):
    users = User.objects.all()
    clients = Client.objects.all()
    quotations = Quotation.objects.all()

    top_sellers = []
    top_clients = []
    products = {}

    for quotation in quotations:
        for product in ProductOnQuotation.objects.filter(quotation=quotation):
            listeroni = str(product).split('*')
            name = listeroni[0]
            number = listeroni[1]
            
            if name in products.keys():
                new_value = products.get(name) + int(number)
                products[name] = new_value
            else:
                products[name] = int(number)

    sorted_products = sorted(products.items(), key=lambda x:x[1], reverse=True)

    for user in users:
        top_sellers.append((user.username, Quotation.objects.filter(user=user).count()))

    sorted_list = sorted(top_sellers, key=lambda tup: tup[1], reverse=True)

    for client in clients:
        top_clients.append((client.name, Quotation.objects.filter(client=client).count()))

    sorted_list2 = sorted(top_clients, key=lambda tup: tup[1], reverse=True)

    context = {'top_sellers':sorted_list[:5], 'top_clients':sorted_list2[:5], 'top_products': sorted_products}

    return render(request, 'analitycs.html', context)