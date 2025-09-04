from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .forms import CodeForm


class CodeConfirmationMixin:
    session_key_data = "pending_data"
    session_key_code = "confirmation_code"
    code_form_class = CodeForm
    initial_form_class = None

    def get_form_class(self):
        if self.session_key_data in self.request.session:
            return self.code_form_class
        return self.initial_form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def handle_initial_form(self, form):
        self.request.session[self.session_key_data] = form.cleaned_data
        self.send_code()
        return redirect(self.request.path)

    def handle_code_form(self, form, pending_data):
        raise NotImplementedError

    def form_valid(self, form):
        if isinstance(form, self.initial_form_class):
            return self.handle_initial_form(form)

        if isinstance(form, self.code_form_class):
            code_entered = form.cleaned_data["code"]
            code_session = self.request.session.get(self.session_key_code)
            pending_data = self.request.session.get(self.session_key_data)

            if not code_session or not pending_data:
                messages.error(self.request, _("No data to confirm. Try again."))
                return redirect(self.request.path)

            if code_entered != code_session:
                messages.error(self.request, _("Incorrect confirmation code."))
                return self.form_invalid(form)

            response = self.handle_code_form(form, pending_data)

            self.request.session.pop(self.session_key_code, None)
            self.request.session.pop(self.session_key_data, None)

            return response

    def send_code(self):
        raise NotImplementedError


class CleanLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return redirect(settings.LOGIN_URL)


class SuperuserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
