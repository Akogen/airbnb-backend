from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from .models import Photo


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise exceptions.NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.host != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise exceptions.PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_200_OK)
