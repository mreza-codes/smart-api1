from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Tell Pydantic to automatically load variables from a '.env' file if it exists
    model_config = SettingsConfigDict(env_file=".env")
    # Default application title (can be overridden by APP_NAME env variable)
    app_name: str = "smart-building-api"
    # Default database connection string (uses local SQLite by default)
    database_url: str = "sqlite:///./app.db"
    # Default logging verbosity level (INFO, DEBUG, ERROR, etc.)
    log_level: str = "INFO"
# Instantiate the settings object so other modules can import and use it
settings = Settings()