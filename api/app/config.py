from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # JWT
    jwt_security_algorithm: str = Field(
        alias="JWT_SECURITY_ALGORITHM",
        default="HS256",
        json_schema_extra={
            "title": "Security Algorithm",
            "description": "The algorithm used for JWT signing. Acceptable values include: HS256, HS384, HS512, RS256, RS384, RS512, ES256, ES384, ES512.",
        },
    )
    jwt_token_timeout_minutes: int = Field(
        alias="JWT_TOKEN_TIMEOUT_MINUTES",
        default=60,
    )
    jwt_security_key: str = Field(
        alias="JWT_SECURITY_KEY",
        json_schema_extra={
            "title": "JWT SECURITY KEY",
            "description": "Generate session key using `openssl rand -base64 32`",
        },
    )
    # Default expire duration in 24hr
    jwt_refresh_token_timeout_minutes: int = Field(
        alias="JWT_REFRESH_TOKEN_TIMEOUT_MINUTES", default=1440
    )

    # EdgeDB
    geldb_host: str = Field(alias="GEL_HOST")
    geldb_port: int = Field(alias="GEL_SERVER_PORT")
    geldb_user: str = Field(alias="GEL_SERVER_USER")
    # 'database' is the instance name
    geldb_instance_name: str = Field(alias="GEL_SERVER_INSTANCE_NAME") 
    
    # 'branch' is the branch name
    geldb_branch_name: str = Field(alias="GEL_SERVER_DEFAULT_BRANCH")
    geldb_tls_security: str = "strict"
    geldb_tls_ca_data: str = Field(alias="GEL_SERVER_TLS_CERT")
    geldb_tls_mode: str = Field(alias="GEL_SERVER_TLS_CERT_MODE")    
    geldb_password: str = Field(alias="GEL_SERVER_PASSWORD")    


    # Build Version
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()