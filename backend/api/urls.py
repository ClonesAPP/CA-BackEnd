
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quotation/<str:pk>', views.quotation, name="quotation"),
    path('create-client/', views.create_client, name="create-client"),
    path('create-quotation/', views.create_quotation, name="create-quotation"),
]