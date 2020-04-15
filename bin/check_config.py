import json


def get_user_config():
    with open("../config/user_config.json", 'r') as load_json:
        user_json = json.load(load_json)
    return user_json


def get_sys_config():
    with open("../config/sys_config.json", 'r') as load_json:
        sys_json = json.load(load_json)
    return sys_json


user_config_json = get_user_config()

sys_config_json = get_sys_config()
