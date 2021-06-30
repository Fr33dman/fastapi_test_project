from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 8000
    database_url: str = 'localhost'
    database_port: int = 6379
