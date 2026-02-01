from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin"
    DB_NAME: str = "sghss_db"

    JWT_SECRET_KEY: str = "sghss_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    @property
    def DATABASE_URL(self):
        return (f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()