from tkinter.constants import CASCADE

from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from . import Author

class Picture(TranslatableModel):
    pictureLink =models.CharField()
    authorId = models.ForeignKey(Author, on_delete=CASCADE, null=False)
    dateOfArrival = models.DateTimeField()
    sizeHorizontal = models.IntegerField()
    sizeVertical = models.IntegerField()
    inStock = models.BooleanField()
    translations = TranslatedFields(
        name = models.CharField(max_length=50),
    )