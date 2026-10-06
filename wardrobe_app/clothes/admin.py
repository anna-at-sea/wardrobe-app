from django.contrib import admin

from .models import ClothingItem


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'created_at',
    )
    search_fields = (
        'name',
        'user__username',
    )