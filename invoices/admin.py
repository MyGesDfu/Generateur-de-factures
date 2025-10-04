from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return f"{obj.get_total_price()}€" if obj.pk else ""
    get_total_price.short_description = 'Total'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'total_amount', 'get_total_items', 'created_at')
    readonly_fields = ('total_amount', 'created_at')
    search_fields = ('invoice_number',)
    inlines = [InvoiceItemInline]

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Nombre d\'articles'


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'unit_price', 'get_total_price')
    list_filter = ('invoice__created_at',)

    def get_total_price(self, obj):
        return f"{obj.get_total_price()}€"
    get_total_price.short_description = 'Total'
