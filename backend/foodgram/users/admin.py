from django.contrib import admin

from .models import CustomUser, Subscription


admin.site.register(Subscription)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')
    list_display = ('email', 'username')
