from django.contrib.auth.forms import PasswordChangeForm

def password_change_form(request):
    if request.user.is_authenticated:
        return {'password_change_form': PasswordChangeForm(user=request.user)}
    return {}