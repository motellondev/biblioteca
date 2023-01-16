from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from django.test import Client
from webapp.models import Book, Author, Category
from django.core.management import call_command

# Create your tests here.
class BookURLTest(LiveServerTestCase):

	@classmethod
	def setUpClass(self):
		super().setUpClass()
		call_command('add_books')
		options = Options()
		options.binary_location = '/usr/bin/brave-browser'
		self.browser = webdriver.Chrome(options = options)
		# driver = webdriver.Chrome(options = options)

	def tearDown(self):
		self.browser.quit()
		super().tearDownClass()

	def test_image(self):
		c = Client()
		books = Book.objects.all()
		print("Testing book images")
		for book in books:
			if book.file_format == "pdf":
				try:
					if book.image == "" or book.image == None:
						print()
						print("Book image NONE")
						print(book.image)
						print(book)
						print()
					else:
						# print('%s/%s' % (self.live_server_url, book.image))
						response = self.browser.get('%s/%s' % (self.live_server_url, book.image))
						self.browser.implicitly_wait(10)
						response = self.browser.get('%s/%s' % (self.live_server_url, book.file))
						self.browser.implicitly_wait(10)
						# Check that the response is 200 OK.
						if "Page not found" in str(self.browser.title):
							print()
							print("Page not found")
							print(book.image)
							print(book)
							print()
				except:
					print()
					print("Exception")
					print(book.image)
					print(book)
					print()





