from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class Birthday(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'Urodziny'


class CustomUserAdmin(UserAdmin):
	inlines = (Birthday,)
	list_display = ('username', 'email', 'first_name', 'last_name', 'get_birthday')
	list_select_related = ('profile',)

	def get_birthday(self, instance):
		return instance.profile.birthday

	get_birthday.short_description = 'Urodziny'

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

