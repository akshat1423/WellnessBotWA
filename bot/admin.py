from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserQuery
from .models import UserGist

class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('phone_no_from','created_at',"message_count",'user_message', 'doctor_response', 'product_response', )
    list_filter = ('user_message','phone_no_from')  # Add filters on the right of the page
    search_fields = ('user_message', 'doctor_response','phone_no_from')  # Add a search bar
    ordering = ('-user_message','phone_no_from')  # Sort by user_message in descending order

    # Custom actions
    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
    mark_as_reviewed.short_description = "Mark selected queries as reviewed"

    actions = [mark_as_reviewed]

class UserGistAdmin(admin.ModelAdmin):
    list_display = ('phone_no_from','created_at', 'gist')
    list_filter = ('phone_no_from',)  # Add filters on the right of the page
    search_fields = ('phone_no_from',)  # Add a search bar
    ordering = ('phone_no_from',)  # Sort by user_message in descending order



admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(UserGist, UserGistAdmin)
