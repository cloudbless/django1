# productsApp/urls.py
from django.urls import path
from . import views

app_name = 'productsApp'

urlpatterns = [
    path('products/<str:productName>/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='productDetail'),
]