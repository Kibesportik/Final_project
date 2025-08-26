from django.shortcuts import render
from .models import Author
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

class AuthorDetail(DetailView):
    template_name= 'author_detail.html'
    model = Author
    context_object_name = 'author'
    slug_url_kwarg = 'author_id'
    slug_field = 'id'

class IndexView(TemplateView):
    template_name = 'index.html'