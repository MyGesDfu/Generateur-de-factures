"""
Script pour ajouter des données de test à l'application
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice_generator.settings')
django.setup()

from products.models import Product
from invoices.models import Invoice, InvoiceItem


def create_sample_data():

    print("Création de produits d'exemple...")

    Product.objects.all().delete()
    Invoice.objects.all().delete()

    products_data = [
        {
            'name': 'Pommes',
            'price': Decimal('2.50'),
            'expiration_date': date.today() + timedelta(days=7)
        },
        {
            'name': 'Pain de mie',
            'price': Decimal('1.80'),
            'expiration_date': date.today() + timedelta(days=3)
        },
        {
            'name': 'Lait entier 1L',
            'price': Decimal('1.20'),
            'expiration_date': date.today() + timedelta(days=5)
        },
        {
            'name': 'Yaourts nature x12',
            'price': Decimal('3.90'),
            'expiration_date': date.today() + timedelta(days=10)
        },
        {
            'name': 'Pâtes spaghetti 500g',
            'price': Decimal('0.95'),
            'expiration_date': date.today() + timedelta(days=365)
        },
        {
            'name': 'Tomates cerises 500g',
            'price': Decimal('3.20'),
            'expiration_date': date.today() + timedelta(days=4)
        },
        {
            'name': 'Fromage râpé 200g',
            'price': Decimal('2.80'),
            'expiration_date': date.today() + timedelta(days=15)
        },
        {
            'name': 'Œufs frais x6',
            'price': Decimal('2.10'),
            'expiration_date': date.today() + timedelta(days=8)
        },
        {
            'name': 'Bananes 1kg',
            'price': Decimal('2.00'),
            'expiration_date': date.today() + timedelta(days=2)
        },
        {
            'name': 'Produit périmé (test)',
            'price': Decimal('5.00'),
            'expiration_date': date.today() - timedelta(days=1)
        }
    ]

    products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        products.append(product)
        print(f"  - {product.name} créé")

    print(f"\n{len(products)} produits créés avec succès!")

    print("\nCréation de factures d'exemple...")

    invoice1 = Invoice.objects.create(invoice_number="FAC-DEMO-001")
    InvoiceItem.objects.create(
        invoice=invoice1,
        product=products[0],
        quantity=2,
        unit_price=products[0].price
    )
    InvoiceItem.objects.create(
        invoice=invoice1,
        product=products[1],
        quantity=1,
        unit_price=products[1].price
    )
    InvoiceItem.objects.create(
        invoice=invoice1,
        product=products[2],
        quantity=2,
        unit_price=products[2].price
    )
    invoice1.calculate_total()
    print(f"  - {invoice1.invoice_number} créée ({invoice1.total_amount}€)")

    invoice2 = Invoice.objects.create(invoice_number="FAC-DEMO-002")
    InvoiceItem.objects.create(
        invoice=invoice2,
        product=products[3],
        quantity=1,
        unit_price=products[3].price
    )
    InvoiceItem.objects.create(
        invoice=invoice2,
        product=products[4],
        quantity=3,
        unit_price=products[4].price
    )
    InvoiceItem.objects.create(
        invoice=invoice2,
        product=products[5],
        quantity=2,
        unit_price=products[5].price
    )
    InvoiceItem.objects.create(
        invoice=invoice2,
        product=products[6],
        quantity=1,
        unit_price=products[6].price
    )
    invoice2.calculate_total()
    print(f"  - {invoice2.invoice_number} créée ({invoice2.total_amount}€)")

    invoice3 = Invoice.objects.create(invoice_number="FAC-DEMO-003")
    InvoiceItem.objects.create(
        invoice=invoice3,
        product=products[7],
        quantity=2,
        unit_price=products[7].price
    )
    InvoiceItem.objects.create(
        invoice=invoice3,
        product=products[8],
        quantity=1,
        unit_price=products[8].price
    )
    invoice3.calculate_total()
    print(f"  - {invoice3.invoice_number} créée ({invoice3.total_amount}€)")

    print("\n✅ Données d'exemple créées avec succès!")
    print("\nVous pouvez maintenant :")
    print("1. Démarrer le serveur: python manage.py runserver")
    print("2. Visiter http://127.0.0.1:8000/ pour voir l'application")
    print("3. Accéder à l'admin sur http://127.0.0.1:8000/admin/ (admin/admin)")


if __name__ == "__main__":
    create_sample_data()