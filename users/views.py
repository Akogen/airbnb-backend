from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from .models import User
from .serializers import PrivateUserSerializer, publicUserSerializer


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        user = serializer.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class Users(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get("password")
        if (not password) or len(password) <= 6:
            raise exceptions.ParseError(
                "Password should be more than 6 characters length with special character."
            )
        serializer = PrivateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        user = serializer.save()
        user.set_password(password)
        user.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class PublicUser(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound

        serializer = publicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise exceptions.ParseError

        if not user.check_password(old_password):
            raise ParseError

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if not user:
            return Response({"error": "Wrong password."})

        login(request, user)
        return Response({"ok": "User login."})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "User logout."})
