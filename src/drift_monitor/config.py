"""Configuration module for drift_monitor detection client."""

from libmytoken import MytokenServer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for drift_monitor detection client."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    DRIFT_MONITOR_DOMAIN: str
    DRIFT_MONITOR_TIMEOUT: int = 10

    DRIFT_MONITOR_MYTOKEN: str
    MYTOKEN_SERVER: str = "https://mytoken.data.kit.edu"

    TESTING: bool = False


# Initialize the settings object
settings = Settings()
mytoken_server = MytokenServer(settings.MYTOKEN_SERVER)
