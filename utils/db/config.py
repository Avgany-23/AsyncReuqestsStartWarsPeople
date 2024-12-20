from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    class Config:
        env_file = ".env"

    POSTGRES_PASSWORD: str = '1234'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = '5432'
    DRIVER: str


psql = PostgresConfig(DRIVER='postgresql+asyncpg')
psql_url = (
    f"{psql.DRIVER}://"
    f"{psql.POSTGRES_USER}:{psql.POSTGRES_PASSWORD}@"
    f"{psql.POSTGRES_HOST}:{psql.POSTGRES_PORT}/{psql.POSTGRES_DB}"
)
