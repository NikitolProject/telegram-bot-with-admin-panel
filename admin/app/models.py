import os

from django.db import models, transaction
from django.utils.safestring import mark_safe, SafeText


class TelegramUser(models.Model):

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'
        db_table = "TelegramUser"

    user_id = models.CharField(max_length=1024)
    chat_id = models.CharField(max_length=1024)
    username = models.CharField(max_length=255, blank=True)

    def get_avatar(self: "TelegramChat") -> str:
        if not os.path.exists(f'{os.getcwd()}/media/{self.user_id}.jpg'):
            return '/media/user.png'
        return f'/media/{self.user_id}.jpg'

    def avatar_tag(self: "TelegramChat") -> SafeText:
        return mark_safe('<img src="%s" width="50" height="50" class="img-circle" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'

    def chat_tag(self: "TelegramUser") -> str:
        return str(TelegramChat.objects.get(chat_id=self.chat_id))

    chat_tag.short_description = 'Chat'

    def __str__(self: "TelegramUser") -> str:
        return f"{self.user_id}:{self.username}"


class TelegramChat(models.Model):

    class Meta:
        verbose_name = 'Телеграм чат'
        verbose_name_plural = 'Телеграм чаты'
        db_table = "TelegramChat"

    chat_id = models.CharField(max_length=1024)
    mention = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True, max_length=255)
    avatar = models.ImageField(blank=True, null=True)

    time_delete_messages_from_bot = models.IntegerField(default=10)

    matfilter = models.BooleanField()
    spamfilter = models.BooleanField()
    captha = models.BooleanField()

    def get_avatar(self: "TelegramChat") -> str:
        if not self.avatar:
            return '/media/chat.png'
        return self.avatar.url

    def avatar_tag(self: "TelegramChat") -> SafeText:
        return mark_safe('<img src="%s" width="50" height="50" class="img-circle" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'

    def users_count(self: "TelegramChat") -> int:
        return TelegramUser.objects.filter(chat_id=self.chat_id).count()

    users_count.short_description = 'Users'
    
    def __str__(self: "TelegramChat") -> str:
        return self.mention


class SwearWord(models.Model):

    class Meta:
        verbose_name = 'Запрещённое слово'
        verbose_name_plural = 'Запрещённые слова'
        db_table = "SwearWord"

    word = models.CharField(max_length=1024)
    chats = models.ManyToManyField(TelegramChat)

    def chats_tag(self: "SwearWord") -> str:
        return ", ".join(str(chat) for chat in self.chats.all())

    chats_tag.short_description = 'Chats'

    def __str__(self: "SwearWord") -> str:
        return self.word


@transaction.atomic
def add_swear_words() -> None:
    with open("words.txt", "r") as f:
        swear_words = f.read().replace("\n", " ").split(", ")
    
    chats = [chat.id for chat in TelegramChat.objects.all()]
    words = []

    for word in swear_words:
        words.append(SwearWord(word=word))

    SwearWord.objects.bulk_create(words)

    for word in SwearWord.objects.all():
        for chat in chats:
            word.chats.add(chat)


# add_swear_words()
