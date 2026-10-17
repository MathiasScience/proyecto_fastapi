"""
Configuración central de la aplicación usando pydantic-settings (Pydantic v2).
Carga variables desde el entorno y desde el archivo .env en la raíz del proyecto.
"""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Metadatos de la app
    app_name: str = Field(default="Mi Proyecto FastAPI", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")

    # Seguridad JWT
    jwt_secret_key: str = Field(default="change_me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=60, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Base de datos
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="mi_base_datos", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="121189", alias="DB_PASSWORD")
    db_min_connections: int = Field(default=1, alias="DB_MIN_CONNECTIONS")
    db_max_connections: int = Field(default=10, alias="DB_MAX_CONNECTIONS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_dsn(self) -> str:
        """Construye un DSN de conexión para asyncpg."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Instancia cacheada de Settings para no releer variables en cada request."""
    return Settings()