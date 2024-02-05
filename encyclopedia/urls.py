from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/NewPage/", views.new_page, name="newpage"),
    path("wiki/ErrorPage/", views.error_page, name="errorpage"),
    path("wiki/random_page.html", views.random_page, name="randompage"),
    path("wiki/<title>", views.title_page, name="titlepage"),
]
