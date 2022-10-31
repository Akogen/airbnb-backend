from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Booking Admin Definition"""

    list_display = (
        "booking_type",
        "user",
        "room",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "guests",
        "created_at",
        "updated_at",
    )

    list_filter = ("booking_type",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )
