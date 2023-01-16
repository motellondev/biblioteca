from django.shortcuts import render
from webapp.models import Book, Category,  Author
from django.core.paginator import Paginator
from django.conf import settings
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.db.models import Count

# Homepage page
def homepage(request):
	books = Book.objects.all().order_by('?')[:8]
	template_name = "webapp/index.html"
	return render(request, template_name, {"books": books})

# Categories page
def categories(request):
    search_category = request.GET.get("search_category")
    if search_category:
        categories = Category.objects.filter(name__icontains=search_category).order_by('name')
    else:
        categories = Category.objects.all().order_by('?')
    paginator = Paginator(categories, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = "webapp/categories.html"
    return render(request, template_name, {"categories": page_obj, "search_category": search_category})


# Category books page
def category_books(request):
    category_name = request.GET.get('category_name')
    category = Category.objects.get(name=category_name)
    books = Book.objects.filter(categories=category).order_by('title').distinct()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = "webapp/category_books.html"
    return render(request, template_name, {"books": page_obj, "category":category})


# Authors page
def authors(request):
    search_author = request.GET.get("search_author")
    if search_author:
        authors = Author.objects.filter(name__icontains=search_author).order_by('name')
    else:
        authors = Author.objects.all().order_by('?')
    paginator = Paginator(authors, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = "webapp/authors.html"
    return render(request, template_name, {"authors": page_obj, "search_author": search_author})


# Author books page
def author_books(request):
    author_name = request.GET.get('author_name')
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(authors=author).order_by('title').distinct()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = "webapp/author_books.html"
    return render(request, template_name, {"books": page_obj, "author":author})


# All books page
def books(request):
    author = request.GET.get('author')
    category = request.GET.get('category')
    categories = Category.objects.all().order_by('name').distinct()
    template_name = "webapp/books.html"
    return render(request, template_name, {"categories": categories, "category": category, "author":author})


#Class for DataTable
class DataTableBooks(BaseDatatableView):
    model = Book
    columns = ['title','authors','categories','pages','file_format']
    order_columns = ['title', 'authors__name']
    max_display_length = 100

    def get_initial_queryset(self):
    	get_categories = self.request.GET.getlist("categories[]")
    	if len(get_categories) > 0:
            books = Book.objects.filter(categories__name__in=get_categories).annotate(count=Count('categories')).filter(count=len(get_categories)).distinct()
            return books
    	else:
            return Book.objects.all().distinct()

    def render_column(self, row, column):
        if column == 'authors':
            return "".join([" - "+a.name for a in row.authors.all()])
        elif column == "categories":
            return "".join([" - "+c.name for c in row.categories.all()])
        elif column == "title":
        	return f'<a href="{row.file}" target=_blank>{row.title}</a>'
        else:
            return super(DataTableBooks, self).render_column(row, column)


    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(categories__name__icontains=search) | Q(authors__name__icontains=search)).distinct()
        return qs
