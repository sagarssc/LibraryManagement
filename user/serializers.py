from .models import User
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'password', 'username','groups')

	def create(self, validated_data):
			validated_data["password"] = make_password(validated_data['password'])
			groups = validated_data.pop("groups")
			user = User(**validated_data)
			user.is_active = True
			user.save()
			user.groups.add(groups[0].id)
			token = Token.objects.get_or_create(user=user)
			return {"id":user.id,"username":user.username, "is_active": user.is_active, "token": str(token[0])}
