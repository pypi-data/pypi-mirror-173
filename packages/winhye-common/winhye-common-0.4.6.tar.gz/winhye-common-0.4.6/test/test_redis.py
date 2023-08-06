import json
import os
import sys

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(PATH)
print(PATH)

from winhye_common.session.session_redis import RedisConnection




def test_redis():
    redis_conn = RedisConnection(
        '121.40.111.33',
        6379,
        1,
        'winhye@1',
    )
    redis_conn.set('111', '111')
    vv = redis_conn.get('111')
    print(vv)
    redis_conn.delete('111')

if __name__ == '__main__':
    test_redis()
