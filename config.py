from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int

    # Указываем, что настройки лежат в файле .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем объект настроек, чтобы использовать его в других файлах
settings = Settings()