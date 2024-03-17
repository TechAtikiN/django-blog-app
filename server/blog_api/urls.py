from django.contrib import admin
from django.urls import path, include
from .views import GetAllBlogsView, GetBlogView, CreateBlogView

urlpatterns = [
    path('create', CreateBlogView.as_view(), name='create'),
    path('', GetAllBlogsView.as_view(), name='get_all'),
    path('<str:id>', GetBlogView.as_view(), name='get'),
]
