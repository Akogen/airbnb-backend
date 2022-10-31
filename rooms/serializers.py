from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Amenity, Facility, HouseRule
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "name",
            "description",
        )


class HouseRuleSerializer(ModelSerializer):
    class Meta:
        model = HouseRule
        fields = (
            "name",
            "description",
        )


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1


class RoomListSerializer(ModelSerializer):
    review_rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "review_rating",
            "is_owner",
            "photos",
        )

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.host == request.user


class RoomDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    review_rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.host == request.user
