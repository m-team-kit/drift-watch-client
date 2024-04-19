"""Configuration module for drift_monitor detection client."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for drift_monitor detection client."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    DRIFT_MONITOR_URL: str
    DRIFT_MONITOR_TIMEOUT: int = 10


# Initialize the settings object
settings = Settings()
