from rest_framework import serializers

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from app.models import SwearWord


class SwearWordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SwearWord
        fields = ("word", "chats")

    word = serializers.CharField(read_only=True)
    chats = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_chats(self: "SwearWordSerializer", obj: "SwearWord") -> list:
        return [chat.chat_id for chat in obj.chats.all()]
