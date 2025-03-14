from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVars(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    DB_URL: str  # Add your database URL here or any other required variables

    model_config = SettingsConfigDict(env_file='.env')


def get_env_vars() -> EnvVars:
    return EnvVars()  # type: ignore
