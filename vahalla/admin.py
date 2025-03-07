from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import MenuItem
from .models import Event

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Event)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title', 'description')