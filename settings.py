from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str

    class Config:
        env_file = ".env"