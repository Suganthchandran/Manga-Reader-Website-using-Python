from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('genre', views.genre, name="genre"),
    path('genre/<slug:name>/', views.genreview, name="genreview"),
    path('genre/<str:cname>/<str:mname>/', views.manga_details, name='manga_details'),
    path('add-to-library/', views.library, name='add_to_library'),
    path('library/', views.manga_library, name="library"),
    path('remove_manga/<int:library_id>/', views.remove_manga, name='remove_manga'),
    path('clear-alert/', views.clear_alert, name='clear_alert'),
    path('search/', views.search, name='search'),
    path('manga/<int:comic_id>/chapter/<int:chapter_number>/', views.chapter_view, name='chapter'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.get_chat, name='get_chat'),
    
]