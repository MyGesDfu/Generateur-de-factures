from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem
from products.models import Product
import uuid


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number']
        widgets = {
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de facture (laissez vide pour auto-génération)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_number'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.invoice_number:
            instance.invoice_number = f"FAC-{uuid.uuid4().hex[:8].upper()}"
        if commit:
            instance.save()
        return instance


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
        }


InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)