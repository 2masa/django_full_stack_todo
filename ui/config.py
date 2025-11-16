from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    fastapi_base_url:str = Field(alias="FASTAPI_BASE_URL")
    flask_security_key:str = Field(alias="FLASK_SECURITY_KEY")
    flask_port:str = Field(alias="FLASK_PORT")
    flask_host:str = Field(alias="FLASK_HOST")
    flask_debug:str = Field(alias="FLASK_DEBUG")
    redis_host:str = Field(alias="REDIS_HOST")
    redis_port:int = Field(alias="REDIS_PORT")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

