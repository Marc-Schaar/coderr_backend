from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("business_user", "reviewer", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("business_user__username", "reviewer__username", "description")
    autocomplete_fields = ("business_user", "reviewer")
