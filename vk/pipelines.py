from .db import Users, Friends


class VkPipeline(object):
    CHUNK = 100  # для оптимизации, будем писать в БД по 100 записей за раз

    def open_spider(self, spider):
        self.users = [] # чтобы не задваивались пользователи
        self.users_to_go = []  # чанк на запись пользователей в БД
        self.friends_to_go = [] # чанк на запись отношений в БД

    def insert(self, lst, Model, force=False):
        # метод для записи чанка в БД
        if lst and (force or len(lst) % self.CHUNK == 0):
            Model.insert_many(lst).execute()
            del lst[:]

    def close_spider(self, spider):
        # по завершению работы спайдера дописываем в БД незаполненые полностью чанки
        self.insert(self.users_to_go, Users, force=True)
        self.insert(self.friends_to_go, Friends, force=True)

    def process_item(self, item, spider):
        # собственно подготовка данных на запись
        if item['id'] not in self.users:
            self.users_to_go.append({'vk_id': item['id'], 'meta': item})
            self.users.append(item['id'])

        if 'parent_id' in item:
            self.friends_to_go.append({'user1_id': item['parent_id'], 'user2_id': item['id']})

        self.insert(self.users_to_go, Users)
        self.insert(self.friends_to_go, Friends)

        return item
