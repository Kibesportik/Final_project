from django.db import models

class Order(models.Model):
    picture = models.ForeignKey("shop.Picture", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    order_confirmation = models.BooleanField()
    dateOfOrder = models.DateTimeField(auto_now_add=True)