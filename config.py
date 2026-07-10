from utils import files_manager
from pydantic_settings import BaseSettings, SettingsConfigDict

files_manager.init_files_root()


class Settings(BaseSettings):
    db_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()