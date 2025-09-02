import random
from django.core.mail import send_mail
from django.utils import translation
from django.utils.translation import gettext as _
from .models import User

def send_email_code(user, request, subject_text=None, message_text=None):
    code = random.randint(100000, 999999)
    request.session['confirmation_code'] = str(code)
    request.session['pending_user_id'] = user.id
    lang = translation.get_language_from_request(request)
    request.session['lang'] = lang

    with translation.override(lang):
        subject = _('Confirmation')
        message = _('Your confirmation code is: {code}').format(code=code)

        send_mail(
            subject,
            message,
            'noreply@myapp.com',
            [user.email],
            fail_silently=False,
        )
