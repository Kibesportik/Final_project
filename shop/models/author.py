from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class Author(TranslatableModel):
    translations = TranslatedFields(
        fullName = models.CharField(max_length=50),
        nickName=models.CharField(max_length=50, null=True, blank=True),
        authorStory = models.TextField()
    )