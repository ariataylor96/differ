from differ import env

REPO_DIRECTORY: str = env.str("REPO_DIRECTORY", default="/repos")

REDIS_URL: str = env.str("REDIS_URL", default="redis://cache:6379/0")
CACHE_CONFIG: dict[str, str] = {
    "CACHE_TYPE": "redis",
    "CACHE_KEY_PREFIX": "differ",
    "CACHE_REDIS_URL": REDIS_URL,
}

DATABASE_URL: str = env.str("DATABASE_URL", default="sqlite:///code/data.db")
