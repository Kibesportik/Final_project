from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    pass

class CodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label=_("Confirmation Code")
    )

class UsernameChangeForm(forms.Form):
    new_username = forms.CharField(
        label=_("New username"),
        max_length = 150,
        required = True
    )
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_new_username(self):
        new_username = self.cleaned_data["new_username"]

        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError(_("This username is already taken."))

        if self.user and self.user.username == new_username:
            raise forms.ValidationError(_("This is already your username."))

        return new_username