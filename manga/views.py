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
from .utils import generate_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .utils import get_user_from_token
from .forms import PasswordResetRequestForm
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
import difflib
import genai
from django.views.decorators.csrf import csrf_exempt
from .demo import gemini

from django.shortcuts import render
from .demo import gemini
from .models import Mangas

def home(request):
    comics = Mangas.objects.filter(trending=True)
    recom = Mangas.objects.filter(recommend=True)
    
    # query = request.GET.get('q')
    # 
    # if not query:
    #     return render(request, "manga/index.html", {
    #         "comics": comics,
    #         "recom": recom,
    #         "res": 'Please enter a search query'
    #     })
    
    # try:
    #     res = gemini(query)  # `res` is now an array of message histories
    #     return render(request, "manga/index.html", {
    #         "comics": comics,
    #         "recom": recom,
    #         "res": [message['parts'][0] for message in res]  # Extracting the text from the history
    #     })
    # except ValueError as e:
    return render(request, "manga/index.html", {"comics": comics,
            "recom": recom,
            # "res": 'An error occurred while processing your request'
        })


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

# def register(request):
#     form = CustomUserForm()
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registration Successful")
#             return redirect('/login')
#     return render(request, "manga/register.html", {'form': form})

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till email confirmation
            user.save()

            # Send confirmation email
            token = generate_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = f'http://{domain}/activate/{uid}/{token}/'
            email_subject = 'Activate your account'
            email_body = render_to_string('manga/activation_email.html', {'user': user, 'link': link})
            send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, "Registration successful! Please check your email to confirm your registration.")
            return redirect('/login')
    return render(request, "manga/register.html", {'form': form})

def activate(request, uidb64, token):
    user = get_user_from_token(uidb64, token, User)
    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('/login')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('/login')
    
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  
            try:
                user = User.objects.get(username=username)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                full_link = f"http://{current_site.domain}{reset_link}"
                subject = "Password Reset Request"
                message = render_to_string('password_reset_email.html', {
                    'user': user,               
                    'reset_link': full_link,
                })
                send_mail(subject, message, None, [user.email])
                return HttpResponse("We have sent you an email with instructions to reset your password.")
            except User.DoesNotExist:
                # Handle the case where the username does not exist
                return HttpResponse("User with this username does not exist.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse("The link is invalid or has expired.")

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
    suggested_query = None
    results = Mangas.objects.all()
    artists = Mangas.objects.values_list('artist', flat=True).distinct()
    authors = Mangas.objects.values_list('author', flat=True).distinct()
    genres = Genre.objects.all()

    # Apply search query filter if present
    if query:
        results = results.filter(name__icontains=query)
        if not results:
            all_manga_names = Mangas.objects.values_list('name', flat=True)
            close_matches = difflib.get_close_matches(query, all_manga_names, n=1, cutoff=0.6)
            if close_matches:
                suggested_query = close_matches[0]
                results = Mangas.objects.filter(name__icontains=suggested_query)

    # Retrieve filter values from the GET request
    artist_filter = request.GET.get('artist')
    author_filter = request.GET.get('author')
    genre_filter = request.GET.get('genres')  # Get the genres as a comma-separated string
    color_filter = request.GET.get('color')
    adaption_filter = request.GET.get('adaption')
    work_status_filter = request.GET.get('work_status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_order = request.GET.get('sort')  # Get the sort order from the request

    # Apply filters if selected
    if artist_filter:
        results = results.filter(artist=artist_filter)
    if author_filter:
        results = results.filter(author=author_filter)

    if genre_filter:
        # Split the genres by commas and convert to a list of integers
        genre_ids = [int(id) for id in genre_filter.split(',') if id.isdigit()]
        if genre_ids:
            results = results.filter(genre__id__in=genre_ids).distinct()

    if color_filter:
        results = results.filter(color=color_filter)
    if adaption_filter:
        results = results.filter(adaption=adaption_filter)
    if work_status_filter:
        if work_status_filter != '':
            results = results.filter(work_status=bool(int(work_status_filter)))
    if start_date:
        results = results.filter(released_date__gte=start_date)
    if end_date:
        results = results.filter(released_date__lte=end_date)

    # Apply sorting based on the selected option
    if sort_order:
        if sort_order == 'A-Z':
            results = results.order_by('name')  # Sort by name A-Z
        elif sort_order == 'Z-A':
            results = results.order_by('-name')  # Sort by name Z-A
        elif sort_order == 'Recently Added':
            results = results.order_by('-created_at')  # Sort by most recently added
        elif sort_order == 'Recently Updated':
            results = results.order_by('-updated_at')  # Sort by most recently updated
        elif sort_order == 'Released Date':
            results = results.order_by('-released_date')  # Sort by released date

    context = {
        'results': results,
        'query': query,
        'suggested_query': suggested_query,
        'display_suggestion': bool(suggested_query) and (query != suggested_query),
        'artists': artists,
        'authors': authors,
        'genres': genres,
        'sort_order': sort_order  # Pass the selected sort order to the template
    }
    return render(request, 'manga/search_results.html', context)


def chapter_view(request, comic_id, chapter_number):
    comics = get_object_or_404(Mangas, id=comic_id)
    chapter = comics.pdf_files.filter(chapter_number=chapter_number).first()
    
    previous_chapter = chapter_number - 1 if chapter_number > 1 else None
    next_chapter = chapter_number + 1 if comics.pdf_files.filter(chapter_number=chapter_number + 1).exists() else None

    context = {
        'comics': comics,
        'chapter_number': chapter_number,
        'chapter': chapter,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter,
    }
    return render(request, 'manga/chapter.html', context)

def get_chat(request):
    return render(request,'manga/chatbot.html')

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        if user_message:
            response_history = gemini(user_message)
            bot_response = response_history[-1]['parts'][0]  # Get the last response from the history
            return JsonResponse({'response': bot_response})
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)