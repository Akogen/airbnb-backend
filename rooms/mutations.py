import typing
import strawberry
from strawberry.types import Info
from django.db import transaction
from enum import Enum
from .models import Room, Amenity
from categories.models import Category


@strawberry.enum
class TypeOfPlaceChoices(Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"
    HOTEL_ROOM = "hotel_room"


@strawberry.enum
class PropertyTypeChoices(Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    GUESTHOUSE = "guesthouse"
    HOTEL = "hotel"


def add_room(
    rooms: int,
    name: str,
    description: str,
    country: str,
    city: str,
    address: str,
    price: int,
    guests: int,
    beds: int,
    bedrooms: int,
    bathrooms: int,
    instant_book: bool,
    pet_friendly: bool,
    type_of_place: TypeOfPlaceChoices,
    property_type: TypeOfPlaceChoices,
    amenities: typing.List[int],
    facilities: typing.List[int],
    house_rules: typing.List[int],
    category_pk: int,
    info: Info,
):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise Exception("The category type should be rooms")
    except Category.DoesNotExist:
        raise Exception(detail="Category does not found.")

    try:
        with transaction.atomic():
            room = Room.objects.create(
                rooms=rooms,
                name=name,
                description=description,
                country=country,
                city=city,
                address=address,
                price=price,
                guests=guests,
                beds=beds,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                instant_book=instant_book,
                type_of_place=TypeOfPlaceChoices,
                property_type=property_type,
                amenities=amenities,
                facilities=facilities,
                house_rules=house_rules,
                category=category,
                owner=info.context.request.user,
            )

            for amenity_pk in amenities:
                amenity = Amenity.objects.get(pk=amenity_pk)
                room.amenities.add(amenity)

            room.save()

            return room
    except Exception:
        raise Exception("amenity does not found.")
