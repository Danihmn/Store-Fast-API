from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str = 'localhost'

    @property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            drivername='postgresql+psycopg2',
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            database=self.DATABASE_NAME,
            host=self.DATABASE_HOST,
        )
