from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """配置信息。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    api_key: str  # GLM API密钥
