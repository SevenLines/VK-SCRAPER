import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase, BinaryJSONField

from .settings import DATABASE_CONNECTION

# настройки подключения к БД
db = PostgresqlExtDatabase(
    register_hstore=False,
    **DATABASE_CONNECTION
)


# базовая модель
class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField()

    class Meta:
        database = db


# пользователи
class Users(BaseModel):
    vk_id = peewee.IntegerField(index=True)
    meta = BinaryJSONField()
    depth = peewee.IntegerField()


# связи между пользователями
class Friends(BaseModel):
    user1_id = peewee.IntegerField(index=True)
    user2_id = peewee.IntegerField(index=True)


# чтоб вручную таблички не создавать, можно будет просто запустить скрипт
if __name__ == '__main__':
    db.create_tables([Users, Friends])
