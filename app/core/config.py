from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database url entry point
    PG_DATABASE_URL: str = "postgresql+psycopg2://root:root@postgres:5432/user_data"

    SECRET_KEY: str = "my_secret_key"

    # For jwt token
    ALGORITHM: str = "HS256"

    # Active full-time for continuous testing
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"


settings = Settings()
