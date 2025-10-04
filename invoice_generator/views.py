from django.shortcuts import render
from products.models import Product
from invoices.models import Invoice


def home_view(request):
    """Vue pour la page d'accueil avec les statistiques"""

    total_products = Product.objects.count()
    total_invoices = Invoice.objects.count()

    recent_products = Product.objects.order_by('-created_at')[:5]
    recent_invoices = Invoice.objects.order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'total_invoices': total_invoices,
        'recent_products': recent_products,
        'recent_invoices': recent_invoices,
    }

    return render(request, 'home.html', context)