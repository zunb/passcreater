from bin.character import character
from bin.check_config import user_config_json, sys_config_json
from bin.clip import clip_copy

import sqlite3
import uuid
import time
import getpass


def Process_entry(url):
    original_url = url  # 体验无GUI请使用input函数
    # print("执行了Process_entry", url, original_url)
    calculate_url = character(original_url=original_url)
    if calculate_url == 1:
        return ["请不要使用非url记录!", 2]
    else:
        Call = Query_Call(calculate_url=calculate_url, original_url=original_url)
        return Call


def Inexistence_Call(calculate_url, original_url):  # 不存在调用
    C_uuid = str(uuid.uuid1())[0:8]
    D_uuid = str(uuid.uuid4())[-12:]
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    insert_basetable_sql = sys_config_json["insert_basetable_sql"].format(C_uuid,
                                                                          time.strftime("%Y-%m-%d", time.localtime()),
                                                                          time.strftime("%H:%M:%S", time.localtime()),
                                                                          original_url,
                                                                          calculate_url, getpass.getuser())

    insert_passtable_sql = sys_config_json["insert_passtable_sql"].format(C_uuid, D_uuid, 1)
    clip_copy(PassWord=D_uuid)
    cursor.execute(insert_basetable_sql)
    cursor.execute(insert_passtable_sql)
    cursor.close()
    conn.commit()
    conn.close()
    # print("执行了Inexistence_Call")
    return D_uuid


def Exist_Call(calculate_url, original_url):  # 存在调用
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    select_basetable_sql = sys_config_json["select_basetable_sql"].format(calculate_url)
    cursor.execute(select_basetable_sql)
    rows = cursor.fetchall()
    Call_uuid = rows[0][0]
    cursor.close()
    conn.commit()
    conn.close()
    # print("执行了Exist_Call")
    return Query_PassWord(Call_uuid=Call_uuid)


def Query_Call(calculate_url, original_url):
    # print("收到了", calculate_url)
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    select_basetable_sql = sys_config_json["select_basetable_sql"].format(calculate_url)
    cursor.execute(select_basetable_sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    # print(select_basetable_sql)
    # print("执行了Query_Call")
    # print(rows)
    if len(rows) > 0:
        return [Exist_Call(calculate_url=calculate_url, original_url=original_url), 1]
    else:
        return [Inexistence_Call(calculate_url=calculate_url, original_url=original_url), 0]


def Query_PassWord(Call_uuid):
    select_passtable_sql = sys_config_json["select_passtable_sql"].format(Call_uuid)
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    cursor.execute(select_passtable_sql)
    rows = cursor.fetchall()
    PassWord = rows[0][1]
    clip_copy(PassWord=PassWord)
    cursor.close()
    conn.commit()
    conn.close()
    return rows[0][1]
