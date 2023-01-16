from django.db import models
from django.contrib import admin


# Create your models here.
class Author(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Categories"


class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField(Author)
	categories = models.ManyToManyField(Category)
	file_format = models.CharField(max_length=10)
	pages = models.IntegerField()
	file = models.FileField()
	image = models.ImageField()

	def __str__(self):
		return self.title

