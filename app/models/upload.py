from datetime import datetime

from pony.orm import PrimaryKey, Required, Optional, composite_key

from app.core.db import db


class Upload(db.Entity):
    id = PrimaryKey(int, auto=True)
    file_name = Required(str, volatile=True)
    md5_hash = Required(str, volatile=True)
    file_path = Required(str, volatile=True)
    note = Optional(str, volatile=True, nullable=True)
    create_time = Required(datetime, default=datetime.now, sql_default='CURRENT_TIMESTAMP', volatile=True)
    update_time = Required(datetime, default=datetime.now, sql_default='CURRENT_TIMESTAMP', volatile=True)




