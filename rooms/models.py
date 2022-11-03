from django.db import models
from django.urls import reverse
from common.models import AbstractTimeStamp


class AbstractItem(AbstractTimeStamp):
    """AbstractItem Object Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Room(AbstractTimeStamp):
    """Room Model Definition"""

    class TypeOfPlaceChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")
        HOTEL_ROOM = ("hotel_room", "Hotel Room")

    class PropertyTypeChoices(models.TextChoices):
        HOUSE = ("house", "House")
        APARTMENT = ("apartment", "Apartment")
        GUESTHOUSE = ("guesthouse", "Guesthouse")
        HOTEL = ("hotel", "Hotel")

    name = models.CharField(
        max_length=180,
        default="",
    )
    description = models.TextField(
        max_length=150,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=80,
        default="United States of America",
    )
    city = models.CharField(
        max_length=80,
        default="Los Angeles",
    )
    address = models.CharField(
        max_length=250,
        default="",
    )
    price = models.PositiveIntegerField()

    guests = models.PositiveIntegerField()
    beds = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()

    check_in = models.TimeField()
    check_out = models.TimeField()

    instant_book = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=True)
    type_of_place = models.CharField(
        max_length=20,
        choices=TypeOfPlaceChoices.choices,
    )

    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="users",
    )

    property_type = models.CharField(
        max_length=20,
        choices=PropertyTypeChoices.choices,
    )

    amenities = models.ManyToManyField(
        "Amenity",
        blank=True,
        related_name="amenities",
    )
    facilities = models.ManyToManyField(
        "Facility",
        blank=True,
        related_name="facilities",
    )
    house_rules = models.ManyToManyField(
        "HouseRule",
        blank=True,
        related_name="house_rules",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="categories",
    )

    def __str__(self) -> str:
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def review_rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in self.reviews.all().values("rating"):
            total_rating += review["rating"]
        return round(total_rating / count, 2)

    review_rating.short_description = "Rating"

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})


class Amenity(AbstractItem):
    """Amentiy Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRules Model Definition"""

    class Meta:
        verbose_name = "House Rule"
