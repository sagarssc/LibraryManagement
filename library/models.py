from django.db import models
from user.models import User
# Create your models here.

class Book(models.Model):
	name = models.CharField(max_length=50, null=False, unique=True)
	available_books = models.IntegerField(null=False)
	is_deleted = models.BooleanField(default = False)

	def is_available(self):
		return True if self.available_books > 0  else False

class BorrowedBooks(models.Model):
	book = models.ForeignKey(Book, related_name = 'borrowers', on_delete=models.CASCADE)
	borrowed_by = models.ForeignKey(User, related_name = 'borrowed_books', on_delete=models.CASCADE)
	is_returned = models.BooleanField(default = False)

	def borrow(self, borrower, book):
		borrowd = BorrowedBooks.objects.create(
			book = book,
			borrowed_by = borrower
		)
		book.available_books -= 1
		book.save() 
		return borrowd
	
	def return_book(self):
		self.is_returned = True
		self.save()
		self.book.available_books += 1
		self.book.save()