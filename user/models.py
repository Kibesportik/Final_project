from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    postcode = models.IntegerField()
    favouritesList =models.CharField()
    inMailingList = models.BooleanField()