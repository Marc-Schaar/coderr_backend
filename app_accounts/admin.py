from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "type",
        "is_staff",
        "is_active",
    )
    list_filter = BaseUserAdmin.list_filter + ("type",)
    fieldsets = BaseUserAdmin.fieldsets + (("Coderr", {"fields": ("type",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Coderr", {"fields": ("type",)}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "tel", "working_hours", "created_at")
    list_filter = ("location",)
    search_fields = ("user__username", "user__email", "location")
