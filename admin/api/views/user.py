from __future__ import annotations

from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import permissions

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from api.serializers.user import TelegramUserSerializer

from app.models import TelegramUser


@extend_schema(description='User create', tags=['telegram'])
class CreateTelegramUser(CreateAPIView):
    model = TelegramUser
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TelegramUserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = TelegramUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
