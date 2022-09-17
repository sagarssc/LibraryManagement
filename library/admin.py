from django.contrib import admin

from .models import Book, BorrowedBooks

class BookAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'available_books',
		'is_deleted',
		)

class BorrowedBooksAdmin(admin.ModelAdmin):
	list_display = (
		'get_book',
		'get_borrower',
		'is_returned',
		)
	def get_book(self, obj):
		return obj.book.name
	
	def get_borrower(self, obj):
		return obj.borrowed_by.username


admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBooks, BorrowedBooksAdmin)
