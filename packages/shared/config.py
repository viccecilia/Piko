from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Piko"
    stage: str = "stage_1_platform_skeleton"
    database_url: str = "postgresql+psycopg://piko:piko@localhost:5432/piko"
    redis_url: str = "redis://localhost:6379/0"
    publishing_enabled: bool = False
    enable_real_connectors: bool = False
    live_connector_test: bool = False
    enable_discovery_real_source: bool = False
    live_discovery_test: bool = False
    connector_timeout_seconds: float = 5.0
    connector_user_agent: str = "PikoBot/0.1 source-policy-contact-required"
    steam_discovery_url: str | None = None
    reddit_discovery_url: str | None = None
    jp_community_discovery_url: str | None = None
    kr_community_discovery_url: str | None = None
    serp_discovery_url: str | None = None
    real_market_max_sources: int = 5
    real_market_max_records_per_source: int = 20
    enable_llm_writer: bool = False
    live_llm_test: bool = False
    llm_model: str = "gpt-4.1-mini"
    llm_timeout_seconds: float = 20.0

    model_config = SettingsConfigDict(env_prefix="PIKO_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
