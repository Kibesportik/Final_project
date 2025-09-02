from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('change_password/', views.PasswordChange.as_view(), name="change_password"),
    path('change_username/', views.UsernameChange.as_view(), name="change_username"),
    path('account_details/<int:user_id>/', views.AccountDetails.as_view(), name="account_details"),
    path("favourites/<int:user_id>/", views.FavouritesView.as_view(), name="favourites"),
    path("cart/<int:user_id>/", views.CartView.as_view(), name="cart"),
    path("cart/delete/<int:pk>/", views.ListDelete.as_view(list_type="cartList"),name="cart_delete"),
    path("favourites/delete/<int:pk>/", views.ListDelete.as_view(list_type="favouritesList"), name="favourites_delete"),
]