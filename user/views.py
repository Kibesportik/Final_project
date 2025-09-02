from .models import User
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UserLoginForm
from .mixins import CleanLoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from .utils import send_email_code
from django.views.generic.edit import CreateView, FormView, DeleteView, View
from django.views.generic.list import ListView
from django.contrib.auth import update_session_auth_hash
from .forms import CodeForm, UsernameChangeForm
from .mixins import CodeConfirmationMixin
from shop.models import Picture, Order
from shop.forms import OrderForm

class Register(CreateView):
    template_name = 'register.html'
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('account_details', kwargs={'user_id': self.request.user.id})


class Login(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('account_details', kwargs={'user_id': self.request.user.id})

class AccountDetails(CleanLoginRequiredMixin,DetailView):
    template_name= 'account_details.html'
    model = User
    context_object_name = 'user'
    slug_url_kwarg = 'user_id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.get_object()
        context['user_orders'] = Order.objects.filter(user=current_user)
        return context

class PasswordChange(CleanLoginRequiredMixin, CodeConfirmationMixin, FormView):
    template_name = "change_password.html"
    initial_form_class = PasswordChangeForm
    code_form_class = CodeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.get_form_class() == PasswordChangeForm:
            kwargs["user"] = self.request.user
        return kwargs

    def send_code(self):
        send_email_code(
            self.request.user,
            self.request,
            subject_text="Password change confirmation",
        )

    def handle_code_form(self, form, pending_data):
        user = self.request.user
        new_password = pending_data["new_password1"]
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(self.request, user)
        return redirect("account_details", user_id=user.id)

    def get_success_url(self):
        return reverse("account_details", kwargs={"user_id": self.request.user.id})


class UsernameChange(CleanLoginRequiredMixin, CodeConfirmationMixin, FormView):
    template_name = "change_username.html"
    initial_form_class = UsernameChangeForm
    code_form_class = CodeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.get_form_class() == UsernameChangeForm:
            kwargs["user"] = self.request.user
        return kwargs

    def send_code(self):
        send_email_code(
            self.request.user,
            self.request,
            subject_text="Username change confirmation",
        )

    def handle_code_form(self, form, pending_data):
        user = self.request.user
        new_username = pending_data["new_username"]
        user.username = new_username
        user.save()
        update_session_auth_hash(self.request, user)
        return redirect("account_details", user_id=user.id)

    def get_success_url(self):
        return reverse("account_details", kwargs={"user_id": self.request.user.id})


class FavouritesView(CleanLoginRequiredMixin,ListView):
    template_name = 'favourites.html'
    model = Picture
    context_object_name = 'favourites_list'
    slug_url_kwarg = 'user_id'
    slug_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if not user.favouritesList:
            return Picture.objects.none()

        return Picture.objects.filter(id__in=user.favouritesList)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class CartView(CleanLoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = Picture
    context_object_name = 'cart_list'
    slug_url_kwarg = 'user_id'
    slug_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if not user.cartList:
            return Picture.objects.none()

        return Picture.objects.filter(id__in=user.cartList)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context["order_form"] = OrderForm()
        return context


class ListDelete(CleanLoginRequiredMixin, View):
    list_type = None

    def post(self, request, *args, **kwargs):
        picture_id = kwargs.get("pk")
        user = request.user

        if not self.list_type:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        user_list = getattr(user, self.list_type, None)

        if user_list and picture_id in user_list:
            user_list.remove(picture_id)
            setattr(user, self.list_type, user_list)
            user.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))
