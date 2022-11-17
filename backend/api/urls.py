
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Rutas de crear, ver cotizacion(es)
    path('quotation/<str:pk>', views.quotation, name="quotation"),
    path('create-quotation/', views.create_quotation, name="create-quotation"),
    path('see-quotations/', views.see_quotations, name="see-quotations"),

    # Rutas CRUD cliente
    path('create-client/', views.create_client, name="create-client"),
    path('see-clients/', views.see_clients, name="see-clients"),
    path('delete-client/<str:client_id>', views.delete_client, name="delete-client"),
    path('update-client/<str:client_id>', views.update_client, name="update-client"),

    # Manejo de sesión, login y logout
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),

    # Rutas CRUD producto
    path('product/<str:pk>', views.product, name="product"),
    path('see-products/', views.see_products, name="see-products"),

    # Creación de producto, para ingresar un producto este requiere crear/seleccionar una categoría y un descuento de ser necesario.
    path('create-product/', views.create_product, name="create-product"),
    path('create-category/', views.create_category, name="create-category"),
    path('create-discount/', views.create_discount, name="create-discount"),
]