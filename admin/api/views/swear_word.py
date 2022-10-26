from __future__ import annotations

from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import permissions

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     UpdateAPIView, ListAPIView)
from rest_framework.response import Response

from api.serializers.swear_word import SwearWordSerializer

from app.models import SwearWord


@extend_schema(description='Swear Word create', tags=['telegram'])
class CreateSwearWordUser(CreateAPIView):
    model = SwearWord
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SwearWordSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = SwearWordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@extend_schema(description="Swear Word get", tags=['telegram'])
class GetSwearWord(ListAPIView):
    model = SwearWord
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SwearWordSerializer
    queryset = SwearWord.objects.all()
