from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    secret_key: str
    expire_time: int
    algorithm: str

    class Config:
        env_file = ".env"


settings = Settings()
