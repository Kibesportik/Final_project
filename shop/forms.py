from .models import Order
from .models import Picture

from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm


class PictureForm(TranslatableModelForm):
    class Meta:
        model = Picture
        fields = ["dateOfArrival", "sizeHorizontal", "sizeVertical"]

    image = forms.ImageField(
        label=_("Image"),
        widget=forms.ClearableFileInput(
            attrs={"class": "real-file-input", "id": "file-input"}
        )
    )
    price = forms.IntegerField(
        label=_("Price in GBP (£)"),
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    sizeHorizontal = forms.FloatField(
        label=_("Width (cm)"),
        min_value=1,
        widget=forms.NumberInput(attrs={"step": "0.1", "class": "form-control"})
    )
    sizeVertical = forms.FloatField(
        label=_("Height (cm)"),
        min_value=1,
        widget=forms.NumberInput(attrs={"step": "0.1", "class": "form-control"})
    )
    dateOfArrival = forms.DateField(
        label=_("Date of Arrival"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )
    name_en = forms.CharField(
        max_length=50,
        label=_("Name (EN)"),
        widget=forms.TextInput(attrs={
            "style": "width:100%;",
            "class": "form-control"
        })
    )
    name_uk = forms.CharField(
        max_length=50,
        label=_("Name (UK)"),
        widget=forms.TextInput(attrs={
            "style": "width:100%;",
            "class": "form-control"
        })
    )
    description_en = forms.CharField(
        label=_("Description (EN)"),
        widget=forms.Textarea(attrs={
            "rows": 5,
            "style": "width:100%;",
            "class": "form-control"
        })
    )
    description_uk = forms.CharField(
        label=_("Description (UK)"),
        widget=forms.Textarea(attrs={
            "rows": 5,
            "style": "width:100%;",
            "class": "form-control"
        })
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "postcode", "order_confirmation"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "50",
                "required": True,
                "placeholder": _("Full name"),
            }),
            "postcode": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "10",
                "required": True,
                "placeholder": _("Postcode"),
            }),
            "order_confirmation": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

        labels = {
            "full_name": _("Full name"),
            "postcode": _("Postcode"),
            "order_confirmation": _("Order confirmation via email"),
        }

