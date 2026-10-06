from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ClothingItem


class ClothingItemForm(forms.ModelForm):

    class Meta:
        model = ClothingItem
        fields = [
            'name',
            'description',
            'image',
        ]
        labels = {
            'name': _("Name"),
            'description': _("Description"),
            'image': _("Image"),
        }
        help_texts = {
            'image': _("Upload a photo of your clothing item."),
        }
