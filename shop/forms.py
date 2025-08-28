from django import forms
from .models import Picture
from parler.forms import TranslatableModelForm

class PictureForm(TranslatableModelForm):
    image = forms.ImageField()
    name_en = forms.CharField(max_length=255, label="Name (EN)")
    name_uk = forms.CharField(max_length=255, label="Name (UK)")

    class Meta:
        model = Picture
        fields = ["author", "dateOfArrival", "sizeHorizontal", "sizeVertical", "inStock", "amount"]

