import sqlite3
from bin.check_config import user_config_json, sys_config_json


def init_database():
    conn = sqlite3.connect(user_config_json["DBPath"])
    create_basetable_sql = sys_config_json["create_basetable_sql"]
    create_passtable_sql = sys_config_json["create_passtable_sql"]
    cursor = conn.cursor()
    cursor.execute(create_basetable_sql)
    cursor.execute(create_passtable_sql)
    cursor.close()
    conn.commit()
    conn.close()





init_database()