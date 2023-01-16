from django.core.management.base import BaseCommand
from os import listdir, path # path.isfile(), path.join(), path.basename()
from django.conf import settings
from django.contrib.auth.models import User
from webapp.models import Author, Category, Book
from pikepdf import Pdf
from pdf2image import convert_from_path
import time

ALL_AUTHORS_PATH = path.join(settings.BASE_DIR, "media/authors_folder")

class Command(BaseCommand):
    def handle(self, **options):
        start_time = time.time()
        self.create_users()
        self.save_authors(ALL_AUTHORS_PATH)
        end_time = time.time()
        total_time = start_time - end_time
        print("--- %s seconds ---" % (total_time))
        print("--- %s minutes ---" % (total_time/60))
        #print()

    def create_users(self):
        User.objects.create_superuser(username="1", email="", password="1")


    def save_authors(self, all_authors_path):
        print("Saving books...")
        for author_path in listdir(all_authors_path):
            # Get authors
            # print(author_path)
            authors = author_path.split(" - ")
            book_authors = []
            for author_name in authors:
                # print(author_name)
                author_name = author_name.rstrip().lstrip()
                try:
                    author = Author.objects.get(name=author_name)
                except Author.DoesNotExist: 
                    author = Author(name=author_name)
                    author.save()
                finally:
                    book_authors.append(author)
            # Look into author's folder
            self.save_books(author_path, book_authors)
        print("All books saved")
            # print()



    def save_books(self, author_path, book_authors):
        books_path = path.join(ALL_AUTHORS_PATH, author_path)
        for book in listdir(books_path):
            book_path = path.join(books_path, book)
            # Get format and remove it from file name
            # print(book)
            book_pages = 0
            book_image = None
            if ".pdf" in book:
                try:
                    # Get pages number
                    pdf = Pdf.open(book_path)
                    book_pages = len(pdf.pages)
                    # Create first pdf page image
                    image_abs_path = book_path.replace(book, "")
                    image_abs_path += "{}{}".format("images/", book.replace("pdf", "jpg"))
                    if path.isfile(image_abs_path):
                        pass 
                    else:
                        pages = convert_from_path(book_path, first_page=0, last_page=1)
                        pages[0].save(image_abs_path, "JPEG")
                    book_image = "{}/{}/{}{}".format("media/authors_folder", author_path, "images/", book.replace("pdf", "jpg"))
                    book_image = str(book_image).replace("?","%3F")
                except Exception as err:
                    print(book)
                    print(f"Unexpected {err=}, {type(err)=}")
                # Title
                book_title = book.replace(".pdf","").rstrip().lstrip()
                # Format
                book_format = "pdf"
            elif ".djvu" in book:
                book_title = book.replace(".djvu","").rstrip().lstrip()
                book_format = "djvu"

            elif ".epub" in book:
                book_title = book.replace(".epub","").rstrip().lstrip()
                book_format = "epub"
            else:
                author_image = book
                # TODO: add ImageField for author
                continue

            # Get cateogries
            book_split = book_title.split(" @")
            title = book_split[0]
            categories_strings = book_split[1:]
            categories = []
            for category in categories_strings:
                category = category.rstrip().lstrip()
                try:
                    categ = Category.objects.get(name=category)
                except Category.DoesNotExist:
                    categ = Category(name=category)
                    categ.save()
                finally:
                    categories.append(categ)

            # print(title)
            # print(categories)
            media_path = path.join("media/authors_folder", author_path)
            file_path = str(path.join(media_path, book)).replace("?","%3F")
            
            book_obj = Book(title=title, file_format=book_format, pages=book_pages, file=file_path, image=book_image)
            book_obj.save()
            [book_obj.authors.add(author) for author in book_authors]
            [book_obj.categories.add(category) for category in categories]
            # print()