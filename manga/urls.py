from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('genre',views.genre,name="genre"),
    path('genre/<str:name>',views.genreview,name="genre"),
]