from vk.db import *

if __name__ == '__main__':
    r = Users.select().where(Users)[:100]
    print(r.data)