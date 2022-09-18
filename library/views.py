from django.http import JsonResponse
from .models import Book, BorrowedBooks
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
	serializer_class = BookSerializer
	
	def get_queryset(self):
		return
	
	@action(detail=False,methods=['post'],permission_classes=[IsAuthenticated])
	def add_book(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		if user.is_librarian():
			serializer = self.get_serializer(data=data)
			serializer.is_valid(raise_exception=True)
			book = serializer.save()
			return JsonResponse(book)
		else:
			raise serializers.ValidationError('User dont have permissions to add book')
	
	@action(detail=True,methods=['put'],permission_classes=[IsAuthenticated])
	def update_book(self, request, pk=None ,*args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		if user.is_librarian():
			books = Book.objects.filter(pk=pk)
			books.update(**data)
			return JsonResponse({"status": "success"})
		else:
			raise serializers.ValidationError('User dont have permissions to update book')

	@action(detail=True,methods=['delete','put'],permission_classes=[IsAuthenticated])
	def remove_book(self, request, pk=None,*args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		if user.is_librarian():
			book = Book.objects.get(pk=pk)
			book.available_books = 0
			book.is_deleted = True
			book.save()
			return JsonResponse({"status": "success"})
		else:
			raise serializers.ValidationError('User dont have permissions to remove book')

class BorrowViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.filter(is_deleted=False)

	@action(detail=False,methods=['get'],permission_classes=[IsAuthenticated])
	def get_books(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		borrowd_books = list(BorrowedBooks.objects.filter(borrowed_by_id=user.id, is_returned=False).values_list('book_id',flat=True))
		queryset = self.get_queryset()
		books = BookSerializer(queryset, many=True).data
		for book in books:
			if book['id'] in  borrowd_books:
				book['status'] = "BORROWED"
		return JsonResponse(books, safe=False)

	@action(detail=False,methods=['put'],permission_classes=[IsAuthenticated])
	def borrow_book(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		book = Book.objects.get(id=data["book_id"])
		if book.available_books > 0:
			borrowed_book = BorrowedBooks()
			borrowed_book.borrow(user, book)
			return JsonResponse({"status":"success"})
		else:
			return JsonResponse({"status":"failed","msg":"Book is not available"})

	
	@action(detail=False,methods=['put'],permission_classes=[IsAuthenticated])
	def return_book(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		borrowed_book = BorrowedBooks.objects.filter(borrowed_by=user, book_id=data["book_id"], is_returned=False).last()
		borrowed_book.return_book()
		return JsonResponse({"status":"success"})
