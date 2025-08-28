from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class Picture(TranslatableModel):
    image = models.URLField()
    author = models.ForeignKey("shop.Author", on_delete=models.CASCADE)
    dateOfArrival = models.DateTimeField()
    sizeHorizontal = models.IntegerField()
    sizeVertical = models.IntegerField()
    inStock = models.BooleanField()
    amount = models.IntegerField()
    translations = TranslatedFields(
        name = models.CharField(max_length=50),
    )