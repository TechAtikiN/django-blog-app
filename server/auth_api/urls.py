from django.contrib import admin
from django.urls import path, include
from auth_api.views import RegisterView, LoginView, UserView, LogoutView, RefreshTokenView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('refresh_token', RefreshTokenView.as_view())
]
