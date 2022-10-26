from django.contrib import admin
from django.http import HttpRequest
from django.db import models

from typing import Any

from requests import post

from app.models import TelegramUser, TelegramChat, SwearWord


def delete_user(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: models.QuerySet) -> None:
    for idx, obj in enumerate(queryset):
        post(
            "http://127.0.0.1:8888/jsonrpc", 
            json={
                "jsonrpc": "2.0",
                "method": "delete_user_from_chat",
                "params": {
                    "user_id": obj.user_id, 
                    "chat_id": obj.chat_id
                },
                "id": idx
            }
        )
        obj.delete()


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'username', 'chat_tag')
    list_filter = ('chat_id',)
    readonly_fields = ('user_id', 'username', 'chat_id')
    list_per_page = 10
    actions = (delete_user,)

    delete_user.short_description = 'Удалить выбранных Телеграм пользователей'

    def has_add_permission(self, request: HttpRequest, obj: TelegramUser = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: TelegramUser = ...) -> bool:
        return False

    # def has_change_permission(self, request, obj: TelegramUser = None) -> bool:
    #     return False


class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'mention', 'title', 'users_count')
    fieldsets = (
        (
            'Главные параметры', {
                'fields': (
                    'chat_id', 'mention', 'title', 
                    'description', 'avatar'
                )
            }
        ),
        (
            'Параметры модерации', {
                'fields': (
                    'time_delete_messages_from_bot',
                    'matfilter', 'spamfilter', 'captha'
                )
            }
        )
    )
    list_per_page = 10

    def save_model(self, request: HttpRequest, obj: TelegramUser, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)

        if change:
            res = post(
                "http://127.0.0.1:8888/jsonrpc", 
                json={
                    "jsonrpc": "2.0",
                    "method": "update_chat",
                    "params": {
                        "chat_id": obj.chat_id,
                        "title": obj.title,
                        "description": obj.description,
                        "avatar": str(obj.avatar)
                    },
                    "id": 1
                }
            )
            print(res.json())

    # def has_add_permission(self, request, obj: TelegramChat = None) -> bool:
    #     return False


class SwearWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'chats_tag')
    fieldsets = (
        (
            'Главные параметры', {
                'fields': (
                    'word', 'chats'
                )
            },
        ),
    )
    list_per_page = 10

    def save_model(self, request: HttpRequest, obj: SwearWord, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        print(form)

        if not change:

            res = post(
                "http://127.0.0.1:8888/jsonrpc", 
                json={
                    "jsonrpc": "2.0",
                    "method": "add_swear_word",
                    "params": {
                        "word": obj.word,
                        "chats": [chat for chat in obj.chats.all()]
                    },
                    "id": 1
                }
            )
            print(res.json())


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramChat, TelegramChatAdmin)
admin.site.register(SwearWord, SwearWordAdmin)
