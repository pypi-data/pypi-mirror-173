import redis

__all__ = ['RedisConnection']


class RedisConnection:
    def __init__(self, host, port, db, password):
        self.__poll = redis.ConnectionPool(host=host, port=port, password=password, max_connections=1000, db=db)
        self.__redis = redis.Redis(connection_pool=self.__poll)

    def set(self, key, value, ex=None):
        return self.__redis.set(key, value, ex)

    def get(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return None

    def query_all_redis(self):
        keys = self.__redis.keys()
        result = []
        for k in keys:
            try:
                key = str(k.decode())
                result.append({
                    'key': key,
                    'value': str(self.__redis.get(key).decode('unicode_escape')),
                })
            except:
                pass
        return result

    def delete(self, key):
        if self.__redis.exists(key):
            return self.__redis.delete(key)
        else:
            return None

    def get_conn(self):
        return self.__redis
