from django.db import models
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from ..utils import s3

class Picture(TranslatableModel):
    image_root = models.CharField(max_length=255)
    dateOfArrival = models.DateTimeField()
    sizeHorizontal = models.IntegerField()
    sizeVertical = models.IntegerField()
    price = models.IntegerField()
    inStock = models.BooleanField(default=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=50),
        description = models.TextField(max_length=255),
    )

    @property
    def presigned_url(self):
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": self.image_root},
            ExpiresIn=60 * 60 * 24 * 7,
        )