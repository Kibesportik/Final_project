from django import forms
from .models import Picture, Order
from parler.forms import TranslatableModelForm

class PictureForm(TranslatableModelForm):
    class Meta:
        model = Picture
        fields = ["dateOfArrival", "sizeHorizontal", "sizeVertical"]

    image = forms.ImageField()
    price = forms.IntegerField(label="Price in GBP (£)")
    name_en = forms.CharField(max_length=50, label="Name (EN)")
    name_uk = forms.CharField(max_length=50, label="Name (UK)")
    description_en = forms.CharField(
        label="Description (EN)", widget=forms.Textarea(attrs={"rows": 5, "style": "width:100%;"})
    )
    description_uk = forms.CharField(
        label="Description (UK)", widget=forms.Textarea(attrs={"rows": 5, "style": "width:100%;"})
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "postcode", "order_confirmation"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "50",
                "required": True
            }),
            "postcode": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "10",
                "required": True
            }),
            "order_confirmation via email: ": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
