from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
class AdminUser(UserAdmin):
    ordering = ("id",)
    fieldsets = (
        (
            "User",
            {"fields": ("password",)},
        ),
        (
            "Personal Info",
            {"fields": ("email", "first_name", "last_name", "clinic_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
    readonly_fields = ["date_joined", "last_login"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "clinic_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    list_display = ["id", "email", "clinic_name", "is_staff", "is_active"]
    list_display_links = ["id", "email", "clinic_name"]


admin.site.register(User, AdminUser)
