from aiogram import types

from src.utils.filters import get_swear_words

NUM_BUTTONS = 5
ENTRY_TIME = 300
BAN_TIME = 30

NEW_USER_ADDED = types.ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_invite_users=False,
    can_change_info=False,
    can_pin_messages=False,
)

USER_ALLOWED = types.ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True,
    can_change_info=False,
    can_pin_messages=False,
)

mate = get_swear_words()

d = {
    'а': ['а', 'a', '@'],
    'б': ['б', '6', 'b'],
    'в': ['в', 'b', 'v'],
    'г': ['г', 'r', 'g'],
    'д': ['д', 'd'],
    'е': ['е', 'e'],
    'ё': ['ё', 'e'],
    'ж': ['ж', 'zh', '*'],
    'з': ['з', '3', 'z'],
    'и': ['и', 'u', 'i'],
    'й': ['й', 'u', 'i', 'y'],
    'к': ['к', 'k', 'i{', '|{'],
    'л': ['л', 'l', 'ji'],
    'м': ['м', 'm'],
    'н': ['н', 'h', 'n'],
    'о': ['о', 'o', '0'],
    'п': ['п', 'n', 'p'],
    'р': ['р', 'r', 'p'],
    'с': ['с', 'c', 's'],
    'т': ['т', 'm', 't'],
    'у': ['у', 'y', 'u'],
    'ф': ['ф', 'f'],
    'х': ['х', 'x', 'h' , '}{'],
    'ц': ['ц', 'c', 'u,'],
    'ч': ['ч', 'ch'],
    'ш': ['ш', 'sh'],
    'щ': ['щ', 'sch'],
    'ь': ['ь', 'b'],
    'ы': ['ы', 'bi'],
    'ъ': ['ъ'],
    'э': ['э', 'e'],
    'ю': ['ю', 'io'],
    'я': ['я', 'ya']
}

users_entrance = (
    '{mention}, добро пожаловать в чат!\nНажми на {subject} чтобы получить доступ к сообщениям',
    'А, {mention}, это снова ты? А, извините, обознался. Нажмите на {subject} и можете пройти',
    'Братишь, {mention}, я тебя так долго ждал. Жми на {subject} и пробегай',
    'Разве это не тот {mention}? Тыкай на {subject} и проходи, пожалуйста, мы ждали',
    'Даже не верится, что это ты, {mention}. Мне сказали не пускать ботов, поэтому нажми на {subject}',

    '{mention}, это правда ты? Мы тебя ждали. Или не ты? Настоящий {mention} сможет нажать на {subject}. ' +
    'Докажи, что ты не бот!',
    'Кого я вижу? Это же {mention}! Тыкай на {subject} и можешь идти',
    'Идёт проверка {mention}.\nПроверка почти завершена. Чтобы продолжить, {mention}, пожалуйста нажмите на {subject}',
    'О, {mention}, мы тебя ждали. Докажи что ты не бот и проходи. Для этого нажми на {subject}',
    'Да {mention}, ты меня уже бесишь! А, прошу прощения, обознался. Чтобы я мог вас впустить, нажмите на {subject}'
)

throttled_answers = (
    'Вот чё ты спамишь? Ну всё, я обиделся на {limit} секунд',
    'Админы, я бы забанил этого спамера... Спамершу... В общем ЭТО! А я игнорю это {limit} секунд',
    'Ты сейчас серьёзно? Ну это бан на {limit} с. И даже не пытайся меня отговорить',
    'Да ты шутишь?! А если я буду спамить, приятно тебе будет? Игнор на {limit} секунд.',
    'Да пошёл ты. Пошла. Всё в общем, это конец, {limit} секунд пошло',

    'Да ты можешь меня хоть {limit} секунд не трогать? Задолбали \U0001F620',
    'Опять ты? Не не не. Подожди {limit} секунд хотябы, потом поговорим \U0001F612',
    'Ещё одно сообщение и меня вырвет! Дай мне отойти {limit} секунд \U0001F922',
    'Опять? Блин... Дай мне {limit} секунд \U0001F635',
    'А ты уже спрашивал. Вот не отвечу! \U0001F92A'
)

