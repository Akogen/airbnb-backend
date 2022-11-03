from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from .models import Room, Amenity, Facility, HouseRule
from .serializers import (
    RoomListSerializer,
    RoomDetailSerializer,
    AmenitySerializer,
    FacilitySerializer,
    HouseRuleSerializer,
)
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer

# from medias.serializers import PhotoSerializer, VideoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        amenity = serializer.save()
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        amenity = serializer.save()
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_200_OK)


class Facilities(APIView):
    def get(self, request):
        all_facilities = Facility.objects.all()
        serializer = FacilitySerializer(all_facilities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        facility = serializer.save()
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)


class FacilityDetail(APIView):
    def get_object(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        facility = self.get_object(pk)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def put(self, request, pk):
        facility = self.get_object(pk)
        serializer = FacilitySerializer(
            facility,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        facility = serializer.save()
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def delete(self, request, pk):
        facility = self.get_object(pk)
        facility.delete()
        return Response(status=status.HTTP_200_OK)


class HouseRules(APIView):
    def get(self, request):
        all_houserules = HouseRule.objects.all()
        serializer = HouseRuleSerializer(all_houserules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseRuleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        houserule = serializer.save()
        serializer = HouseRuleSerializer(houserule)
        return Response(serializer.data)


class HouseRuleDetail(APIView):
    def get_object(self, pk):
        try:
            return HouseRule.objects.get(pk=pk)
        except HouseRule.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        houserule = self.get_object(pk)
        serializer = HouseRuleSerializer(houserule)
        return Response(serializer.data)

    def put(self, request, pk):
        houserule = self.get_object(pk)
        serializer = HouseRuleSerializer(
            houserule,
            request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        houserule = serializer.save()
        serializer = HouseRuleSerializer(houserule)
        return Response(serializer.data)

    def delete(self, request, pk):
        houserule = self.get_object(pk)
        houserule.delete()
        return Response(status=status.HTTP_200_OK)


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return Response(serializer.errors)

        category_pk = request.data.get("category")
        if not category_pk:
            raise exceptions.ParseError("Category is required.")
        try:
            category = Category.objects.get(pk=category_pk)
            if category.category_type == Category.CatogoryTypeChoices.EXPERIENCES:
                raise exceptions.ParseError("The Category Type should be 'room'.")
        except Category.DoesNotExist:
            raise exceptions.ParseError("Category not found.")

        with transaction.atomic():
            try:
                room = serializer.save(
                    host=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    room.amenities.add(amenity)
            except Exception:
                raise exceptions.ParseError("Amenity not found.")

            try:
                facilities = request.data.get("facilities")
                for facility_pk in facilities:
                    facility = Facility.objects.get(pk=facility_pk)
                    room.facilities.add(facility)
            except Exception:
                raise exceptions.ParseError("facility not found.")

            try:
                house_rules = request.data.get("house_rules")
                for house_rule_pk in house_rules:
                    house_rule = HouseRule.objects.get(pk=house_rule_pk)
                    room.house_rules.add(house_rule)
            except Exception:
                raise exceptions.ParseError("House rule not found.")

        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get_category_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room.host != request.user:
            raise exceptions.PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            request.data,
            partial=True,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        category_pk = request.data.get("category")
        if category_pk:
            try:
                category = self.get_category_object(category_pk)
                if category.category_type == Category.CatogoryTypeChoices.EXPERIENCES:
                    raise exceptions.ParseError("The Category Type should be 'room'.")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found.")
        else:
            category = self.get_category_object(room.category)

        with transaction.atomic():
            try:
                room = serializer.save(
                    host=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")
                if type(amenities) is list:
                    print(type(amenities))
                    print(RoomAmenities)
                    room.amenities.clear()
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
            except Exception:
                raise exceptions.ParseError("Amenity not found.")

            try:
                facilities = request.data.get("facilities")
                if type(facilities) is list:
                    room.facilities.clear()
                    for facility_pk in facilities:
                        facility = Facility.objects.get(pk=facility_pk)
                        room.facilities.add(facility)
            except Exception:
                raise exceptions.ParseError("facility not found.")

            try:
                house_rules = request.data.get("house_rules")
                if type(house_rules) is list:
                    room.house_rules.clear()
                    for house_rule_pk in house_rules:
                        house_rule = HouseRule.objects.get(pk=house_rule_pk)
                        room.house_rules.add(house_rule)
            except Exception:
                raise exceptions.ParseError("House rule not found.")

        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.host != request.user:
            raise exceptions.PermissionDenied
        room.delete()
        return Response(status=status.HTTP_200_OK)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serialzer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serialzer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        review = serializer.save(
            user=request.user,
            room=self.get_object(pk),
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class RoomAmenities(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serialzer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serialzer.data)

    def post(self, request, pk):
        serializer = AmenitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        amenity = serializer.save()
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if room.host != request.user:
            raise exceptions.PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        photo = serializer.save(room=room)
        serialzer = PhotoSerializer(photo)
        return Response(serialzer.data)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            booking_type=Booking.BookingTypeChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)

        serializer = CreateRoomBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        booking = serializer.save(
            room=room,
            user=request.user,
            kind=Booking.BookingKindChoices.ROOM,
        )
        serialzer = CreateRoomBookingSerializer(booking)
        return Response(serialzer.data)
