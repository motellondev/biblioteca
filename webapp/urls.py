from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("categories", views.categories, name="categories"),
    path("category_books", views.category_books, name="category_books"),
    path("authors", views.authors, name="authors"),
    path("author_books", views.author_books, name="author_books"),
    path("books", views.books, name="books"),
    path('books/datatable/', views.DataTableBooks.as_view(), name='books_table'),
]