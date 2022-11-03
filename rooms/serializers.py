from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Amenity, Facility, HouseRule
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


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
    is_host = SerializerMethodField()
    is_liked = SerializerMethodField(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "review_rating",
            "is_host",
            "is_liked",
            "photos",
        )

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.host == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()


class RoomDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    facilities = FacilitySerializer(read_only=True, many=True)
    house_rules = HouseRuleSerializer(read_only=True, many=True)
    review_rating = SerializerMethodField(read_only=True)
    is_host = SerializerMethodField(read_only=True)
    is_liked = SerializerMethodField(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.host == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()
