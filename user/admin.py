from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
	list_display = (
		'username',
		'password',
		'is_active',
		'get_groups'
		)

	def get_groups(self, obj):
		return "\n".join([group.name for group in obj.groups.all()])

admin.site.register(User, CustomUserAdmin)