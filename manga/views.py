from django.shortcuts import render
from . models import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,"manga/index.html")

def register(request):
    return render(request,"manga/register.html")

def genre(request):
    category = Genre.objects.filter(status=0)
    return render(request,"manga/genre.html",{"category":category}) 

def genreview(request,name):
    if(Genre.objects.filter(name=name,status=0)):
        comics = Mangas.objects.filter(genre__name = name)
        return render(request,"manga/comics/index.html",{"comics":comics,"genre_name":name})
    else:
        messages.warning(request,"No such Genre Found")
        return redirect('genre')
