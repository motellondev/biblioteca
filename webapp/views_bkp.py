from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from webapp.models import Book, Category,  Author
from django.core.paginator import Paginator
from django.conf import settings
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.db import models
from django.db import connection
import mimetypes

def homepage(request):
	books = Book.objects.all().order_by('?')[:8]
	template_name = "webapp/index.html"
	return render(request, template_name, {"books": books})

def categories(request):
	categories = Category.objects.all().order_by('?')
	paginator = Paginator(categories, 24)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	template_name = "webapp/categories.html"
	return render(request, template_name, {"categories": page_obj})

def authors(request):
	authors = Author.objects.all().order_by('?')
	paginator = Paginator(authors, 24)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	template_name = "webapp/authors.html"
	return render(request, template_name, {"authors": page_obj})

def books(request, categories=None, author=None):
	categories = Category.objects.all().order_by('name')
	template_name = "webapp/books.html"
	return render(request, template_name, {"categories": categories})


#Classes for DATATABLES
class DataTableBooks(BaseDatatableView):
    model = Book
    columns = ['title','authors','categories','pages','file_format']
    order_columns = ['title', 'authors__name']
    max_display_length = 500

    def get_initial_queryset(self):
    	get_categories = self.request.GET.getlist("categories[]")
    	if len(get_categories) > 0:
    		print("Categories: " + str(get_categories))

    		# filters = models.Q()
    		# for category in get_categories:
    		# 	filters &= models.Q(categories__name=category,)
    		# queryset = Book.objects.filter(filters)
    		# print("Queryset")
    		# print(queryset.query)
    		# return queryset

    		# queryset = Book.objects.all()
    		# for category in get_categories:
    		# 	queryset = queryset.filter(categories__name=category)
    		# print("Queryset")
    		# print(queryset.query)
    		# return queryset

    		# select = 'SELECT * from webapp_book INNER JOIN webapp_category ON (webapp_book_category_id = webapp_category_id) WHERE webapp_category_name IN (Economía)'
    		# queryset = Book.objects.raw(select)
    		# print("Queryset")
    		# print(queryset.query)
    		# return queryset

            # category_names_str = ",".join(["'{}'".format(c) for c in get_categories])
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         '''
            #         SELECT DISTINCT "webapp_book"."id", "webapp_book"."title", "webapp_book"."file_format",
            #          "webapp_book"."pages", "webapp_book"."file", "webapp_book"."image" 
            #          FROM "webapp_book" 
            #          INNER JOIN "webapp_category" ON "webapp_book"."id" IN 
            #          (SELECT "book_id" FROM "webapp_book_categories" 
            #          WHERE "category_id" IN (SELECT "id" FROM "webapp_category" WHERE "name" in (%s)))
            #         '''%category_names_str,
            #         )

            #     rows = cursor.fetchall()

            
            # filters = models.Q()
            # for category in get_categories:
            #     filters &= models.Q(categories__name__icontains=category,)
            # books = Book.objects.filter(filters).distinct()

    		print(books)
    		print(books.query)
    		return books
    	else:
    		return Book.objects.all()

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




# Basándome en ese ejemplo de código Django genera esta consulta SQL que filtra por la categoría "Escuela austriaca" SELECT DISTINCT "webapp_book"."id", "webapp_book"."title", "webapp_book"."file_format", "webapp_book"."pages", "webapp_book"."file", "webapp_book"."image" FROM "webapp_book" INNER JOIN "webapp_book_categories" ON ("webapp_book"."id" = "webapp_book_categories"."book_id") INNER JOIN "webapp_category" ON ("webapp_book_categories"."category_id" = "webapp_category"."id") WHERE "webapp_category"."name" LIKE %Escuela austriaca% ESCAPE '\' y esta me devuelve el siguiente resultado: <QuerySet [<Book: Reseña Jesús Huerta de Soto, Socialismo, Cálculo Económico y Función Empresarial>]>. La siguiente consulta filtra por la categoría "Empreserialidad" SELECT DISTINCT "webapp_book"."id", "webapp_book"."title", "webapp_book"."file_format", "webapp_book"."pages", "webapp_book"."file", "webapp_book"."image" FROM "webapp_book" INNER JOIN "webapp_book_categories" ON ("webapp_book"."id" = "webapp_book_categories"."book_id") INNER JOIN "webapp_category" ON ("webapp_book_categories"."category_id" = "webapp_category"."id") WHERE "webapp_category"."name" LIKE %Empreserialidad% ESCAPE '\' y devuelve el siguiente resultado: <QuerySet [<Book: Reseña Jesús Huerta de Soto, Socialismo, Cálculo Económico y Función Empresarial>, <Book: Naturaleza, Límites y Funcionamiento Interno de las Empresas>]>. Como ves el libro Reseña Jesús Huerta de Soto, Socialismo, Cálculo Económico y Función Empresarial tiene ambas categorías "Empreserialidad" y "Escuela Austriaca". Sin embargo al combinar la consulta: SELECT DISTINCT "webapp_book"."id", "webapp_book"."title", "webapp_book"."file_format", "webapp_book"."pages", "webapp_book"."file", "webapp_book"."image" FROM "webapp_book" INNER JOIN "webapp_book_categories" ON ("webapp_book"."id" = "webapp_book_categories"."book_id") INNER JOIN "webapp_category" ON ("webapp_book_categories"."category_id" = "webapp_category"."id") WHERE ("webapp_category"."name" LIKE %Empreserialidad% ESCAPE '\' AND "webapp_category"."name" LIKE %Socialismo% ESCAPE '\') el resultado es <QuerySet []>. ¿Por que no devuelve dicho libro?



# SOLUCIÓN DEJAR UN SELECT CATEGORY SIMPLE (SOLO UNA OPCIÓN) *quitar librería js multiple select