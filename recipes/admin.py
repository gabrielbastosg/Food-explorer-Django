from django.contrib import admin

from .models import FavoriteRecipe


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'user__username')
    ordering = ('-created_at',)
