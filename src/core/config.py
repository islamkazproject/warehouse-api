from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBHelper(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    url: PostgresDsn
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    products: str = '/products'
    orders: str = '/orders'


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


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
