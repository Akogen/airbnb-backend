from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


class GoodBadFilter(admin.SimpleListFilter):

    title = "Filter by Good or Bad Rating!"

    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        rating = self.value()
        if rating == "good":
            return reviews.filter(rating__gte=3)
        elif rating == "bad":
            return reviews.filter(rating__lt=3)
        else:
            reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin Definition"""

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        GoodBadFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
