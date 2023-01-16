from django.contrib import admin
from .models import Author, Category, Book

# Register your models here.

# Author
class AuthorAdmin(admin.ModelAdmin):
	readonly_fields = ('all_books',)

	def all_books(self,obj):
		return "\n".join(["- "+b.title for b in obj.book_set.all()])

admin.site.register(Author, AuthorAdmin)

# Category
class CategoryAdmin(admin.ModelAdmin):
	readonly_fields = ('all_books',)

	def all_books(self,obj):
		return "\n".join(["- "+b.title for b in obj.book_set.all()])

admin.site.register(Category, CategoryAdmin)


# Book
class BookAdmin(admin.ModelAdmin):
	readonly_fields = ('authors','categories')
	
admin.site.register(Book)
