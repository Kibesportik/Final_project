from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    postcode = models.IntegerField(null=True)
    favouritesList =models.CharField(null=True)
    inMailingList = models.BooleanField(null=True)