from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mysql_host: str
    mysql_port: int = 3306
    mysql_database: str
    mysql_user: str
    mysql_password: str

    llm_provider: str
    llm_model: str
    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()