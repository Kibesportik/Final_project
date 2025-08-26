from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Author

@admin.register(Author)
class AuthorAdmin(TranslatableAdmin):
    list_display = ("fullName", "nickName", "authorStory")