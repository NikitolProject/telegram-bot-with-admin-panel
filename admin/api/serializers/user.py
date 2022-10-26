from rest_framework import serializers

from app.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = "__all__"
