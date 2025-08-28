from django.db import models

class Order(models.Model):
    picture = models.ForeignKey("shop.Picture", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    dateOfOrder = models.DateTimeField()