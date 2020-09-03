from datetime import datetime

from pony.orm import PrimaryKey, Required, Optional, composite_key

from app.core.db import db


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(str)  # 唯一uuid
    name = Optional(str, volatile=True, nullable=True)  # 账户名
    avatar = Optional(str, volatile=True, nullable=True)  # 头像
    email = Required(str, volatile=True, nullable=True)  # 账户邮箱

    introduction = Optional(str, volatile=True, nullable=True)  # 介绍
    roles = Required(str, volatile=True, nullable=True)  # 角色

    phone = Required(str, volatile=True, unique=True)  # 手机号

    hashed_password = Required(str, volatile=True)
    is_active = Required(int, default="1", sql_default="1", volatile=True)
    is_visitor = Required(int, default="0", sql_default="0", volatile=True)
    is_superuser = Required(int, default="0", sql_default="0", volatile=True)

    create_time = Required(datetime, default=datetime.now, sql_default='CURRENT_TIMESTAMP', volatile=True)
    update_time = Required(datetime, default=datetime.now, sql_default='CURRENT_TIMESTAMP', volatile=True)

    composite_key(name, phone)


    # roles: ['admin'],
    # introduction: 'I am a super administrator',
    # avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    # name: 'Super Admin'

