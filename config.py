from typing import Dict, Tuple

import redis
import dotenv
import os
import json


# Load env variables from file
dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DATABASE_URL = os.getenv('DATABASE_URL')

r = redis.Redis(
    host=os.getenv('redis_host'),
    port=os.getenv('redis_port'),
    password=os.getenv('redis_password'),
)


USERS_SEARCHING_FOR_GAME = 'users_searching'
if not r.get(USERS_SEARCHING_FOR_GAME):
    print(f"No {USERS_SEARCHING_FOR_GAME}")
    r.set(USERS_SEARCHING_FOR_GAME, b'{}', 3600 * 48)  # 48 hours


def _get_first_el_from_dict(some_dict) -> Tuple:
    for el in some_dict:
        res = some_dict[el]
        del some_dict[el]
        return el, res


def get_searching_users() -> Dict:
    bytes_res = r.get(USERS_SEARCHING_FOR_GAME)
    return json.loads(bytes_res.decode('utf-8'))


def set_searching_users(new_dict: Dict):
    r.set(USERS_SEARCHING_FOR_GAME, json.dumps(new_dict).encode('utf-8'), 3600 * 48)
