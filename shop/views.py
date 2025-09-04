import uuid

from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView

from user.mixins import CleanLoginRequiredMixin, SuperuserRequiredMixin
from .forms import PictureForm, OrderForm
from .models import Picture
from .utils import upload_to_r2


class IndexView(ListView):
    template_name = "index.html"
    model = Picture
    context_object_name = "pictures"
    paginate_by = 8

    def get_queryset(self):
        return Picture.objects.filter(inStock=True)


class UploadPhoto(SuperuserRequiredMixin, CleanLoginRequiredMixin, FormView):
    template_name = "upload.html"
    form_class = PictureForm
    success_url = "/"

    def form_valid(self, form):
        file = form.cleaned_data["image"]
        filename = f"photos/{uuid.uuid4()}_{file.name}"
        image_root = upload_to_r2(file, filename)

        picture = Picture.objects.create(
            image_root=image_root,
            price=form.cleaned_data["price"],
            dateOfArrival=form.cleaned_data["dateOfArrival"],
            sizeHorizontal=form.cleaned_data["sizeHorizontal"],
            sizeVertical=form.cleaned_data["sizeVertical"],
        )

        picture.set_current_language("en")
        picture.name = form.cleaned_data["name_en"]
        picture.description = form.cleaned_data["description_en"]
        picture.save()

        picture.set_current_language("uk")
        picture.name = form.cleaned_data["name_uk"]
        picture.description = form.cleaned_data["description_uk"]
        picture.save()

        return super().form_valid(form)


class PictureDetails(DetailView):
    model = Picture
    template_name = "picture_details.html"
    context_object_name = "picture"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderForm()
        return context


class AddToFavourites(CleanLoginRequiredMixin, UpdateView):
    def get(self, request, pk):
        user = request.user
        if user.favouritesList is None:
            user.favouritesList = []
        if pk not in user.favouritesList:
            user.favouritesList.append(pk)
            user.save()

        return redirect("picture_details", pk=pk)


class AddToCart(CleanLoginRequiredMixin, UpdateView):
    def get(self, request, pk):
        user = request.user
        if user.cartList is None:
            user.cartList = []
        if pk not in user.cartList:
            user.cartList.append(pk)
            user.save()

        return redirect("picture_details", pk=pk)


class AddOrder(CleanLoginRequiredMixin, CreateView):
    form_class = OrderForm

    def get_template_names(self):
        return ["cart.html", "picture_details.html"]

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        picture_id = self.request.POST.get("picture_id")

        if picture_id:
            picture = Picture.objects.get(pk=picture_id)
            order_confirmation = form.cleaned_data.get("order_confirmation", False)
            form.instance.order_confirmation = order_confirmation
            form.instance.picture = picture

            response = super().form_valid(form)

            picture.inStock = False
            picture.save()

            if user.cartList and picture.id in user.cartList:
                user.cartList.remove(picture.id)
            if user.favouritesList and picture.id in user.favouritesList:
                user.favouritesList.remove(picture.id)

            user.save()

            if order_confirmation:
                send_mail(
                    subject=_("Order Confirmation"),
                    message=_(
                        "Confirmation of your order:\n"
                        "Picture name: {name}\n"
                        "Order price: {price} £\n"
                        "Order date: {date}"
                    ).format(
                        name=picture.name,
                        price=picture.price,
                        date=form.instance.dateOfOrder.strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                    from_email="noreply@myapp.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            return response

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", "/")


class PictureSearch(View):
    def get(self, request, *args, **kwargs):
        search_word = request.GET.get("search_word", "").strip()

        if search_word:
            pictures = Picture.objects.filter(
                Q(
                    translations__language_code="en",
                    translations__name__icontains=search_word,
                )
                | Q(
                    translations__language_code="uk",
                    translations__name__icontains=search_word,
                ),
                inStock=True,
            ).distinct()
        else:
            pictures = Picture.objects.none()

        data = [
            {
                "id": picture.id,
                "name_en": picture.safe_translation_getter(
                    "name", language_code="en"
                ),
                "name_uk": picture.safe_translation_getter(
                    "name", language_code="uk"
                ),
                "price": picture.price,
                "sizeHorizontal": picture.sizeHorizontal,
                "sizeVertical": picture.sizeVertical,
                "presigned_url": picture.presigned_url,
            }
            for picture in pictures
        ]

        return JsonResponse(data, safe=False)
