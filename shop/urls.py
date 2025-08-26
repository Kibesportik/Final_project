from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("author/<int:author_id>/", views.AuthorDetail.as_view(), name="author_detail"),
]