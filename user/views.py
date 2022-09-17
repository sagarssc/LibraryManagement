from django.http import JsonResponse
from .models import User
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

class UserViewSet(viewsets.ModelViewSet):
	serializer_class = RegisterSerializer
	# http_method_names = ['post']

	@action(detail=False, methods=["post"],permission_classes=[])
	def register(self, request, pk=None, *args, **kwargs):
		data = request.data
		data["groups"] = list(Group.objects.filter(name=data["group"]).values_list("id",flat=True))
		if data.get("groups"):
			serializer = self.get_serializer(data=data)
			serializer.is_valid(raise_exception=True)
			user_data = serializer.save()
			return JsonResponse(user_data)
		else:
			raise serializers.ValidationError('Please provide valid user group.')

	@action(detail=False,methods=['post'],permission_classes=[])
	def login(self, request, *args, **kwargs):
		data = request.data
		user = authenticate(username = data.get("username"),password = data.get("password"))
		if user and user.is_active:
			user.remove_token()
			token = Token.objects.get_or_create(user=user)
			return JsonResponse({
				"id":user.id,"username":user.username, "is_active": user.is_active, "token": str(token[0])
			})
		else:
			raise serializers.ValidationError('Incorrect Credentials Passed.')

	@action(detail=False,methods=['put'],permission_classes=[IsAuthenticated])
	def remove_member(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		member = User.objects.get(id=data["member_id"])
		if user.is_librarian():
			if (not member.is_librarian()):
				member.is_active = False
				member.save()
				member.remove_token()
				return JsonResponse({"status":"success"})
			else:
				raise serializers.ValidationError('you cant remove librarian')
		else:
			raise serializers.ValidationError("you don't have permissions to remove member")

	@action(detail=False,methods=['put'],permission_classes=[IsAuthenticated])
	def delete_account(self, request, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		user.is_active = False
		user.save()
		user.remove_token()
		return JsonResponse({"status":"success"})
		# raise serializers.ValidationError('Incorrect Credentials Passed.')