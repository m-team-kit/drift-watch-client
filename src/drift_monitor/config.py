"""Configuration module for drift_monitor detection client."""

from libmytoken import MytokenServer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for drift_monitor detection client."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    DRIFT_MONITOR_URL: str
    DRIFT_MONITOR_TIMEOUT: int = 10

    MYTOKEN_SERVER: str = "https://mytoken.data.kit.edu"


# Initialize the settings object
settings = Settings()
mytoken_server = MytokenServer(settings.MYTOKEN_SERVER)
