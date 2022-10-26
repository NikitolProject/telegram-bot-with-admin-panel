from pony import orm

db = orm.Database()


class TelegramUser(db.Entity):
    user_id = orm.Required(str)
    chat_id = orm.Required(str)
    username = orm.Optional(str)


class TelegramChat(db.Entity):
    chat_id = orm.Required(str)
    mention = orm.Required(str)
    title = orm.Optional(str)
    description = orm.Optional(str)
    avatar = orm.Optional(str)

    time_delete_messages_from_bot = orm.Optional(int)

    matfilter = orm.Required(bool)
    spamfilter = orm.Required(bool)
    captha = orm.Required(bool)


db.bind(provider='sqlite', filename='../../../admin/db.sqlite3', create_db=False)
db.generate_mapping(create_tables=True)
