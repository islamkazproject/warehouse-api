from typing import Optional, Dict, Any

from pydantic import PostgresDsn, Field, field_validator, BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    pg_host: str = Field("0.0.0.0", env="POSTGRES_HOST")
    pg_port: str = Field(8000, env="POSTGRES_PORT")
    pg_db: str = Field("db", env="POSTGRES_DB")
    pg_user: str = Field("postgres", env="POSTGRES_USER")
    pg_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    url: Optional[PostgresDsn] = None
    echo: bool = False,
    echo_pool: bool = False,
    pool_size: int = 50,
    max_overflow: int = 10,

    @field_validator("url", mode='before')
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get('pg_user'),
            password=values.get("pg_password"),
            host=values.get("pg_host"),
            port=values.get("pg_port"),
            path=f'/{values.get("pg_db") or ""}'
        )


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: str = '8000'


class ApiPrefix(BaseModel):
    prefix: str = '/api/v1'


class Settings(BaseSettings):
    project_name: str = 'Warehouse API'
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DBSettings

    class Config:
        case_sensitive = True


settings = Settings()
