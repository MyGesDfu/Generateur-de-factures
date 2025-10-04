from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Invoice, InvoiceItem
from products.models import Product
from .forms import InvoiceForm, InvoiceItemFormSet
import json


@login_required
def invoice_list(request):
    search_query = request.GET.get('search', '')
    invoices = Invoice.objects.all()

    if search_query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search_query) |
            Q(total_amount__icontains=search_query)
        )

    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'invoices/invoice_list.html', context)


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.invoiceitem_set.all()

    context = {
        'invoice': invoice,
        'items': items,
    }
    return render(request, 'invoices/invoice_detail.html', context)


@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()

            selected_products = request.POST.getlist('selected_products')
            quantities = request.POST.getlist('quantities')

            product_quantities = {}

            for i, product_id in enumerate(selected_products):
                if product_id and i < len(quantities) and quantities[i]:
                    try:
                        quantity = int(quantities[i])
                        if quantity > 0:
                            if product_id in product_quantities:
                                product_quantities[product_id] += quantity
                            else:
                                product_quantities[product_id] = quantity
                    except ValueError:
                        continue

            for product_id, total_quantity in product_quantities.items():
                try:
                    product = Product.objects.get(pk=product_id)
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=total_quantity,
                        unit_price=product.price
                    )
                except Product.DoesNotExist:
                    continue

            invoice.calculate_total()

            messages.success(request, f'La facture {invoice.invoice_number} a été créée avec succès.')
            return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        preselected_product_id = request.GET.get('product')

    products = Product.objects.all().order_by('name')

    context = {
        'form': form,
        'products': products,
        'preselected_product_id': preselected_product_id,
    }
    return render(request, 'invoices/invoice_form.html', context)


@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()

            invoice.invoiceitem_set.all().delete()

            selected_products = request.POST.getlist('selected_products')
            quantities = request.POST.getlist('quantities')

            product_quantities = {}

            for i, product_id in enumerate(selected_products):
                if product_id and i < len(quantities) and quantities[i]:
                    try:
                        quantity = int(quantities[i])
                        if quantity > 0:
                            if product_id in product_quantities:
                                product_quantities[product_id] += quantity
                            else:
                                product_quantities[product_id] = quantity
                    except ValueError:
                        continue

            for product_id, total_quantity in product_quantities.items():
                try:
                    product = Product.objects.get(pk=product_id)
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=total_quantity,
                        unit_price=product.price
                    )
                except Product.DoesNotExist:
                    continue

            invoice.calculate_total()

            messages.success(request, f'La facture {invoice.invoice_number} a été modifiée avec succès.')
            return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)

    products = Product.objects.all().order_by('name')
    existing_items = invoice.invoiceitem_set.all()

    context = {
        'form': form,
        'products': products,
        'invoice': invoice,
        'existing_items': existing_items,
    }
    return render(request, 'invoices/invoice_form.html', context)


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'La facture {invoice_number} a été supprimée avec succès.')
        return redirect('invoices:invoice_list')

    return render(request, 'invoices/invoice_confirm_delete.html', {'invoice': invoice})


@require_http_methods(["GET"])
def get_product_price(request):
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = Product.objects.get(pk=product_id)
            return JsonResponse({
                'price': float(product.price),
                'name': product.name,
                'expired': product.is_expired()
            })
        except Product.DoesNotExist:
            pass

    return JsonResponse({'error': 'Produit non trouvé'}, status=404)
