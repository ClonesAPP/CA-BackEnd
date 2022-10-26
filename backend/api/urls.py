
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quotation/<str:pk>', views.quotation, name="quotation"),
    path('create-client/', views.create_client, name="create-client"),
    path('create-quotation/', views.create_quotation, name="create-quotation"),
    path('see-quotations/', views.see_quotations, name="see-quotations"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
]