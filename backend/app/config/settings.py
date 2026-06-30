from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from .env.
    """

    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    class Config:
        env_file = ".env"


settings = Settings()