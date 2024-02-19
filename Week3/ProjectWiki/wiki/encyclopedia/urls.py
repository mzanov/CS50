from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>", views.entryPage, name="entry_page"),
    path('search/', views.searchResults, name='search_results'),
    path('createPage/', views.createNewPage, name='create_new_page'),
    path("edit/<str:title>/", views.editEntry, name="edit_entry"),
    path("random/", views.randomEntry , name="random_entry")
]
