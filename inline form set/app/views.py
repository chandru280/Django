from django.shortcuts import render

# Create your views here.
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from .models import Product
from .forms import  ProductForm, ProductMetaInlineFormset


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)

        context['product_meta_formset'] = ProductMetaInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_meta_formset = ProductMetaInlineFormset(self.request.POST)
        if form.is_valid() and product_meta_formset.is_valid():
            return self.form_valid(form, product_meta_formset)
        else:
            return self.form_invalid(form, product_meta_formset)

    def form_valid(self, form, product_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_metas = product_meta_formset.save(commit=False)
        for meta in product_metas:
            meta.product = self.object
            meta.save()
        return redirect(reverse("product:product_list"))

    def form_invalid(self, form, product_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  product_meta_formset=product_meta_formset
                                  )
        )
    






