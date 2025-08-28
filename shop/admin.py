from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Author
from .models import Picture

@admin.register(Author)
class AuthorAdmin(TranslatableAdmin):
    list_display = ("fullName", "nickName", "authorStory")

@admin.register(Picture)
class PictureAdmin(TranslatableAdmin):
    list_display = ("image",
                    "author",
                    "dateOfArrival",
                    "sizeHorizontal",
                    "sizeVertical",
                    "inStock",
                    "amount",
                    "name",
                    )

