from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from wardrobe_app import utils

from .forms import ClothingItemForm
from .models import ClothingItem


class ClothingItemListView(
    utils.UserLoginRequiredMixin,
    ListView,
):
    model = ClothingItem
    template_name = 'pages/clothes/clothing_item_list.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        return ClothingItem.objects.filter(
            user=self.request.user
        )


class ClothingItemDetailView(
    utils.UserLoginRequiredMixin,
    DetailView,
):
    model = ClothingItem
    template_name = 'pages/clothes/clothing_item_detail.html'
    context_object_name = 'clothing_item'

    def get_queryset(self):
        return ClothingItem.objects.filter(
            user=self.request.user
        )


class ClothingItemCreateView(
    utils.UserLoginRequiredMixin,
    CreateView,
):
    model = ClothingItem
    form_class = ClothingItemForm
    template_name = 'layouts/base_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(
            self.request,
            _("Clothing item was added successfully.")
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': _("Add Clothing Item"),
            'button_text': _("Add"),
        })

        return context

    def get_success_url(self):
        return reverse_lazy(
            'clothing_item_detail',
            kwargs={'pk': self.object.pk},
        )


class ClothingItemUpdateView(
    utils.UserLoginRequiredMixin,
    UpdateView,
):
    model = ClothingItem
    form_class = ClothingItemForm
    template_name = 'layouts/base_form.html'

    def get_queryset(self):
        return ClothingItem.objects.filter(
            user=self.request.user
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Clothing item was updated successfully.")
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': _("Edit Clothing Item"),
            'button_text': _("Save"),
        })

        return context

    def get_success_url(self):
        return reverse_lazy(
            'clothing_item_detail',
            kwargs={'pk': self.object.pk},
        )


class ClothingItemDeleteView(
    utils.UserLoginRequiredMixin,
    DeleteView,
):
    model = ClothingItem
    template_name = 'layouts/base_form.html'

    def get_queryset(self):
        return ClothingItem.objects.filter(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': _("Delete Clothing Item"),
            'delete_prompt': _(
                "Are you sure you want to delete this clothing item?"
            ),
            'button_text': _("Yes, delete"),
        })

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Clothing item was deleted successfully.")
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clothing_item_list')
