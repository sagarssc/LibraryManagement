from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from rest_framework.authtoken.models import Token

# Create your models here.


class User(AbstractUser):
	name = models.CharField(max_length=50, null=False)
	password = models.CharField(max_length=100, null=False)
	is_active = models.BooleanField(default = True)
	groups = models.ManyToManyField(Group, related_name="user_set")

	def is_librarian(self):
		return self.groups.filter(name = 'Librarian').exists()

	def remove_token(self):
		is_tokened = Token.objects.filter(user=self).exists()
		if is_tokened:
			self.auth_token.delete()