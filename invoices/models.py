from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from products.models import Product


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de facture")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Montant total (€)"
    )

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-created_at']

    def __str__(self):
        return f"Facture {self.invoice_number} - {self.total_amount}€"

    def calculate_total(self):
        total = sum(item.get_total_price() for item in self.invoiceitem_set.all())
        self.total_amount = total
        self.save()
        return total

    def get_total_items(self):
        return sum(item.quantity for item in self.invoiceitem_set.all())


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="Facture")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantité"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire (€)"
    )

    class Meta:
        verbose_name = "Article de facture"
        verbose_name_plural = "Articles de facture"

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def get_total_price(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
        self.invoice.calculate_total()
