from django.contrib import admin
from django.urls import path, include
from .views import GetAllBlogsView, CreateBlogView, GetBlogView

urlpatterns = [
    path('', GetAllBlogsView.as_view()),
    path('<str:id>', GetBlogView.as_view()),
    path('create', CreateBlogView.as_view())
]
