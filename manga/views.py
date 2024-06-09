from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from manga.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

def home(request):
    comics = Mangas.objects.filter(trending=True)
    recom = Mangas.objects.filter(recommend=True)
    return render(request, "manga/index.html", {"comics": comics, "recom": recom})

def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid UserName or Password")
            return redirect("/login")
    return render(request, "manga/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You are logged out successfully!")
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/')

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('/login')
    return render(request, "manga/register.html", {'form': form})

def genre(request):
    category = Genre.objects.filter(status=False)
    return render(request, "manga/genre.html", {"category": category})

def genreview(request, name):
    if Genre.objects.filter(name=name, status=False).exists():
        comics = Mangas.objects.filter(genre__name=name)
        return render(request, "manga/comics/index.html", {"comics": comics, "genre_name": name})
    else:
        messages.warning(request, "No such Genre Found")
        return redirect('genre')

def manga_details(request, cname, mname):
    mname = mname.replace('%20', ' ')
    if Genre.objects.filter(name=cname, status=False).exists():
        if Mangas.objects.filter(name=mname, status=False).exists():
            comics = Mangas.objects.filter(name=mname, status=False).first()
            pdf_files = comics.pdf_files.all()
            return render(request, "manga/comics/manga_details.html", {"comics": comics, 'pdf_files': pdf_files})
        else:
            messages.error(request, 'No Such Manga Found')
            return redirect('genre')
    else:
        messages.error(request, 'No Such Genre Found')
        return redirect('genre')


def library(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                manga_id = data.get('bid')
                user = request.user
                manga = Mangas.objects.get(id=manga_id)
                if Library.objects.filter(user=user, book=manga).exists():
                    return JsonResponse({'status': 'Manga Already in Library'}, status=200)
                else:
                    Library.objects.create(user=user, book=manga)
                    return JsonResponse({'status': 'Manga Added to Library'}, status=200)
            except Mangas.DoesNotExist:
                return JsonResponse({'status': 'Manga Not Found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        else:   
            return JsonResponse({'status': 'Login to Add to Library'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)
    
def manga_library(request):
    if request.user.is_authenticated:
        library = Library.objects.filter(user=request.user)
        alert_displayed = request.session.pop('alert_displayed', False)
        return render(request, "manga/library.html", {"library": library, "alert_displayed": alert_displayed})
    else:
        return redirect('/login')

@require_POST
def remove_manga(request, library_id):
    if request.user.is_authenticated:
        Library.objects.filter(id=library_id).delete()
        request.session['alert_displayed'] = True
        return redirect('/library')
    return redirect('/login')

@require_POST
def clear_alert(request):
    if request.user.is_authenticated:
        request.session.pop('alert_displayed', None)
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'unauthorized'}, status=401)

def search(request):
    query = request.GET.get('q')
    results = Mangas.objects.filter(name__icontains=query) if query else []
    return render(request, 'manga/search_results.html', {'results': results, 'query': query})
