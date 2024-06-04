from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('genre',views.genre,name="genre"),
    path('genre/<slug:name>/', views.genreview, name="genre"),
    path('genre/<slug:cname>/<slug:mname>', views.manga_details, name="manga_details"),
]