import aioredis
from settings import Settings


settings = Settings()


class RedisConnector:
    def __init__(self):
        conn = aioredis.ConnectionsPool((settings.database_url, settings.database_port), minsize=1, maxsize=200000)
        self.connector = aioredis.Redis(conn)
