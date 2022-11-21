from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random_page/", views.random_page, name="random_page")
]

# Personal notes
""" 
Line 7: use property <str:name>
    path("<str:name>", views.greet, name="greet") --> this is the path in the URL
    You can use this but adjust it to our variable'title' (instead of 'name') 
    to refer with the URL
    Source: https://cs50.harvard.edu/web/2020/notes/3/
"""
