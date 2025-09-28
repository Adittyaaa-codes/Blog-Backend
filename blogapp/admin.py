from django.contrib import admin
from .models import Blog

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	list_display = ('user_name', 'caption', 'created_at')

	def user_name(self, obj):
		return obj.user.username
	user_name.short_description = 'User Name'

admin.site.register(Blog, BlogAdmin)