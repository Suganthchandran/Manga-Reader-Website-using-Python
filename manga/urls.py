from django.urls import path,re_path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),    
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('genre',views.genre,name="genre"),
    path('genre/<slug:name>/', views.genreview, name="genre"),
    # path('genre/<slug:cname>/<slug:mname>', views.manga_details, name="manga_details"),
    re_path(r'^genre/(?P<cname>[-a-zA-Z0-9_]+)/(?P<mname>[-a-zA-Z0-9_ ]+)$', views.manga_details, name="manga_details"),
    path('add-to-library/', views.library, name='add_to_library'),
    path('library/', views.manga_library, name="library"),
    path('remove_manga/<int:library_id>/', views.remove_manga, name='remove_manga'),
    path('clear-alert/', views.clear_alert, name='clear_alert'),
    path('search/', views.search, name='search'),
    
]