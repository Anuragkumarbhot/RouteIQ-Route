import redis
import json
import os

REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

try:

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True
    )

    redis_client.ping()

    REDIS_AVAILABLE = True

except Exception:

    REDIS_AVAILABLE = False


def cache_get(key):

    if not REDIS_AVAILABLE:

        return None

    data = redis_client.get(key)

    if data:

        return json.loads(data)

    return None


def cache_set(key, value):

    if not REDIS_AVAILABLE:

        return

    redis_client.set(
        key,
        json.dumps(value),
        ex=3600
    )
