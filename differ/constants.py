from urllib.parse import urlparse
from differ import env
from redis import Redis

REDIS_URL = env.str("REDIS_URL", default="redis://cache:6379/0")

REPO_DIRECTORY = env.str("REPO_DIRECTORY", default="/repos")
CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_KEY_PREFIX": "differ",
    "CACHE_REDIS_URL": REDIS_URL,
}
REDIS_CONNECTION = Redis(host=urlparse(REDIS_URL).hostname)
