from .models import Book
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class BookSerializer(serializers.ModelSerializer):
	# is_available = serializers.SerializerMethodField()

	class Meta:
		model = Book
		fields = ('id', 'name', 'available_books')

	def to_representation(self, obj):
		data = {
			"id": obj.id,
			"name": obj.name,
			"status": "AVAILABLE" if obj.is_available else "Not AVAILABLE"
		}
		return data

	def create(self, validated_data):
			book = Book(**validated_data)
			book.save()
			return {"id":book.id,"name":book.name}
