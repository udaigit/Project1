from django.urls import path

from . import views
#The "name=" parameter in path() function is usually used to refer to the URL for that page in "href=" attribute.
urlpatterns = [
    
    path("", views.index, name="index"),
    path("wiki/newpage/", views.new_page, name="newpage"),
    #path("wiki/errorpage/", views.error_page, name="errorpage"),
    path("wiki/randompage", views.random_page, name="randompage"),
    path("wiki/searchpage", views.search_page, name="searchpage"),
    path("wiki/editpage/<entry>", views.edit_page, name="editpage"),
    path("wiki/<title>", views.title_page, name="titlepage"),
]
