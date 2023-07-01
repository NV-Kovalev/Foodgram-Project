from django.contrib import admin
from .models import CustomUser, Subscriptions

admin.site.register(Subscriptions)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')
    list_display = ('email', 'username')
