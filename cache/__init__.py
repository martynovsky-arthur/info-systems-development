import json

from redis import Redis, DataError, ConnectionError


class RedisCache:
    def __init__(self, config: dict):
        self.config = config

    @property
    def conn(self):
        return Redis(**self.config)

    def set_value(self, name: str, value_dict: dict, ttl: float):
        value_json = json.dumps(value_dict)
        try:
            self.conn.set(name=name, value=value_json)
            if ttl > 0:
                self.conn.expire(name, ttl)
                return True
        except DataError as err:
            print(f'{__name__ = }: {err = }')
            return False

    def get_value(self, name: str):
        value_json = self.conn.get(name)
        if not value_json:
            return None
        value_dict = json.loads(value_json)
        return value_dict
