from django.contrib import admin
from .models import Room, Amenity, Facility, HouseRule


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {
                "classes": ("wide"),
                "fields": (
                    "category",
                    "name",
                    "description",
                    "country",
                    "address",
                    "price",
                ),
            },
        ),
        (
            "Times",
            {
                "classes": ("wide"),
                "fields": (
                    "check_in",
                    "check_out",
                    "instant_book",
                ),
            },
        ),
        (
            "Spaces",
            {
                "classes": ("wide"),
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "bathrooms",
                ),
            },
        ),
        (
            "Mores about the space",
            {
                "classes": ("collapse", "wide"),
                "fields": (
                    "type_of_place",
                    "property_type",
                    "amenities",
                    "facilities",
                ),
            },
        ),
        (
            "House Rules",
            {
                "classes": ("collapse", "wide"),
                "fields": (
                    "pet_friendly",
                    "house_rules",
                ),
            },
        ),
        (
            "Host",
            {"fields": ("host",)},
        ),
    )

    actions = (reset_prices,)

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "bathrooms",
        "total_amenities",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "review_rating",
    )

    ordering = (
        "name",
        "country",
        "price",
        "bedrooms",
        "beds",
        "bathrooms",
    )

    list_filter = (
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "bathrooms",
        "check_in",
        "check_out",
        "instant_book",
        "host",
    )

    search_fields = (
        "name",
        "=city",
        "^price",
        "^host__username",
    )

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_facilities(self, obj):
        return obj.facilities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    def count_house_rules(self, obj):
        return obj.house_rules.count()


@admin.register(Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
