from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __init__(self) -> None:
        super().__init__()

    AUTHENTICATION_ENABLED: bool = Field(default=True)
    REQUIRED_ROLE: str = Field(default="Role.User")

    AZURE_CLIENT_ID: str = Field(default="dd7e115a-037e-4846-99c4-07561158a9cd")
    AZURE_TENANT_ID: str = Field(default="3aa4a235-b6e2-48d5-9195-7fcf05b459b0")

    API_HOST_IP: str = Field(default="0.0.0.0")
    PORT: int = Field(default=3017)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SARA_SAP_",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
