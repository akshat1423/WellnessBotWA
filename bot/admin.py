from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserQuery

class UserQueryAdmin(admin.ModelAdmin):
    list_display = ['user_message', 'doctor_response', 'product_response']

admin.site.register(UserQuery, UserQueryAdmin)
