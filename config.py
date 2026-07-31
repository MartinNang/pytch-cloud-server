from utils import files_manager
from pydantic_settings import BaseSettings, SettingsConfigDict

files_manager.init_files_root()


class Settings(BaseSettings):
    db_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expiry_time: int
    jwt_refresh_token_expiry_time: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()