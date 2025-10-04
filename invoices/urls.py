from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('create/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('api/product-price/', views.get_product_price, name='get_product_price'),
]