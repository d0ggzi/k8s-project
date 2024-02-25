from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    JWT_SECRET: str

    POSTGRES_OUT_HOST: str
    POSTGRES_OUT_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL_psycopg(self):
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_OUT_HOST}:{self.POSTGRES_OUT_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
