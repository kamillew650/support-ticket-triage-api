from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_connection_string: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()