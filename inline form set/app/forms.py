from cProfile import Profile
from django import forms
from django.forms import inlineformset_factory

from .models import  Product, ProductMeta


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price')


class ProductMetaForm(forms.ModelForm):
    class Meta:
        model = ProductMeta
        fields = ('name', 'value')


ProductMetaInlineFormset = inlineformset_factory(
    Product,
    ProductMeta,
    form=ProductMetaForm,
    extra=5,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)














