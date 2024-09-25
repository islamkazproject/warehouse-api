from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBHelper(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    url: PostgresDsn


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = '/api/v1'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        env_prefix='API_CONFIG__',
        case_sensitive=False,
    )

    project_name: str = 'Warehouse API'
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DBHelper


settings = Settings()
