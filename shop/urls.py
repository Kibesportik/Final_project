from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('add/picture/', views.UploadPhoto.as_view(), name='upload_photo'),
    path('add/tofavourites/<int:pk>/', views.AddToFavourites.as_view(), name='add_to_favourites'),
    path('add/tocart/<int:pk>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('new/order/', views.AddOrder.as_view(), name='new_order'),
    path("product-search/", views.PictureSearch.as_view(), name="picture_search"),
    path("picture_details/<int:pk>/", views.PictureDetails.as_view(), name="picture_details"),
]