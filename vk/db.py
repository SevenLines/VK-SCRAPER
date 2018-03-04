import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase, BinaryJSONField

# настройки подключения к БД
db = PostgresqlExtDatabase(
    database='vk_parse',
    user="m",
    password="12345",
    register_hstore=False
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


# связи между пользователями
class Friends(BaseModel):
    user1_id = peewee.IntegerField(index=True)
    user2_id = peewee.IntegerField(index=True)


# чтоб вручную таблички не создавать, можно будет просто запустить скрипт
if __name__ == '__main__':
    db.create_tables([Users, Friends])
