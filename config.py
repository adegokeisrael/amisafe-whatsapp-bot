from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    whatsapp_token: str
    whatsapp_phone_number_id: str
    whatsapp_api_version: str = "v19.0"
    verify_token: str
    encryption_key: str
    database_url: str = "sqlite:///./amisafe.db"
    partner_api_key: str
    media_temp_dir: str = "/tmp/amisafe_media"
    session_ttl: int = 1800
    log_level: str = "INFO"

    @property
    def whatsapp_api_url(self) -> str:
        return f"https://graph.facebook.com/{self.whatsapp_api_version}/{self.whatsapp_phone_number_id}/messages"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Ensure media temp dir exists
os.makedirs(settings.media_temp_dir, exist_ok=True)
