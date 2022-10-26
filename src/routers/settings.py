from pydantic import BaseSettings


class Settings(BaseSettings):

    DATASET_STORAGE_BASE_URL: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379

    DATASET_STORAGE_BASE_URL: str = "file:///datasets/"

    CONFIG_STORAGE_BASE: str = "file:///dojo/configs/"

    UVICORN_RELOAD: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
