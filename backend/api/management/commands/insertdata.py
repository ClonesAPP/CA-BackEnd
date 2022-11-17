import pandas as pd
from api.models import Product, ProductCategory, Discount, Client
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import random

possible_discounts = ["Sin descuento", "Verano", "Invierno"]

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # DATA INSERT FOR CLIENT TABLE
        client_data = pd.read_excel('insert_data.xlsx')
        for name, surname, email, identification, address, phone, cell_number, city in zip(
            client_data.name, client_data.surname, client_data.email, client_data.identification, client_data.address,
            client_data.phone, client_data.cell_phone, client_data.city):
            curr_client = Client(name=name, surname=surname, email=email, identification=identification, address=address,
                                phone=phone, cell_number=cell_number, city=city)

            curr_client.save()
        

        # DATA INSERT FOR PRODUCT CATEGORIES

        categories = pd.read_excel('insert_data.xlsx', sheet_name="categorias")

        for name, description in zip(categories.name, categories.description):
            product_category = ProductCategory(name=name, description=description)
            product_category.save()

        # DATA INSERT DISCOUNT
        discounts = pd.read_excel('insert_data.xlsx', sheet_name="descuento")

        for name, description, discount_percentage, active in zip(
            discounts.name, discounts.description, discounts.discount_percentage, discounts.active):

            discount = Discount(name=name, description=description, discount_percentage=discount_percentage, active=active)
            discount.save()

    
        # DATA INSERT PRODUCT
        products = pd.read_excel('insert_data.xlsx', sheet_name="productos")

        for category, name, price, specifications in zip(
            products.category, products.name, products.price, products.specifications):

            curr_category = get_object_or_404(ProductCategory, name=category)
            discount = get_object_or_404(Discount, name=random.choice(possible_discounts))
            

            product = Product(category=curr_category, name=name, price=price, specifications=specifications, discount=discount)
            product.save()

