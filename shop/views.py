import uuid
from .models import Author, Picture
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .r2_utils import upload_to_r2
from parler.utils.context import switch_language
from .forms import PictureForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.conf import settings

def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, "author_detail.html", {"author": author})

# class AuthorDetail(DetailView):
#     template_name= 'author_detail.html'
#     model = Author
#     context_object_name = 'author'
#     slug_url_kwarg = 'author_id' # что именно мы ищем в роуте
#     slug_field = 'id' # в какой колонке мы это ищем

class IndexView(ListView):
    template_name = 'index.html'
    model = Picture
    context_object_name = 'pictures'


def upload_photo(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['image']
            filename = f"photos/{uuid.uuid4()}_{file.name}"
            url = upload_to_r2(file, filename)
            picture = Picture.objects.create(image=url,
                                           author = form.cleaned_data['author'] ,
                                           dateOfArrival=form.cleaned_data['dateOfArrival'] ,
                                           sizeHorizontal= form.cleaned_data['sizeHorizontal'] ,
                                           sizeVertical= form.cleaned_data['sizeVertical'],
                                           inStock= form.cleaned_data['inStock'] ,
                                           amount= form.cleaned_data['amount'],
                                           )
            picture.set_current_language('en')
            picture.name = form.cleaned_data['name_en']
            picture.save()

            picture.set_current_language('uk')
            picture.name = form.cleaned_data['name_uk']
            picture.save()
            return redirect('/')
    else:
        form = PictureForm()

    return render(request, 'upload.html', {'form': form})