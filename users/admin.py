from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms import models as rooms_models
from . import models


# class PhotoInline(admin.StackedInline):
class RoomInline(admin.TabularInline):
    model = rooms_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "avatar",
                    "email",
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "name",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "is_host",
                ),
                "classes": ("wide"),
            },
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
                ),
                "classes": ("collapse", "wide"),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse", "wide"),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "name",
        "gender",
        "language",
        "currency",
        "is_active",
        "is_host",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )
