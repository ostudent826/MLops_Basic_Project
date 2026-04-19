"""
Configuration management for the AI Platform.
Uses Pydantic Settings to validate environment variables and external config files.
"""

from pathlib import Path
from pydantic_settings import (
    BaseSettings,
    YamlConfigSettingsSource,
    SettingsConfigDict,
    DotEnvSettingsSource,
)
from pydantic import BaseModel
import os

# Define the root directory of the project for locating .env and config files
base_dir = Path(__file__).parent.parent.parent


class AnthropicSettings(BaseModel):
    """Configuration schema for Anthropic (Claude) models."""

    api_key: str
    model: str = "anthropic/claude-haiku-4-5"


class GeminiSettings(BaseModel):
    """Configuration schema for Google Gemini models."""

    api_key: str
    model: str = "gemini/gemini-2.5-flash"


class ChatgptSettings(BaseModel):
    """Configuration schema for OpenAI ChatGPT models."""

    api_key: str
    model: str = "openai/gpt-4o-mini"


class Settings(BaseSettings):
    """
    Main Settings class that aggregates all configuration parts.
    Loads data from environment variables, .env files, and config.yaml.
    """

    model_config = SettingsConfigDict(
        env_file=base_dir / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # Allows setting nested models via ENV (e.g., ANTHROPIC__API_KEY)
    )

    # General Application Settings
    environment: str = "dev"
    log_level: str = "info"
    api_url: str
    api_timeout: int
    max_retries: int
    backoff_multiplier: int

    # Provider-Specific Settings
    anthropic: AnthropicSettings
    gemini: GeminiSettings
    chatgpt: ChatgptSettings

    # Usage and Budget Constraints
    max_user_token: int
    max_tokens: int = 10000
    max_cost: float = 1  # Currency unit: USD ($)

    # Vector Database / RAG Settings
    db_store_collection: str = "store_default"
    db_persistent: str
    db_query_max_results: int
    chunk_size: int
    chunk_overlap: int

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """
        Defines the priority order for configuration sources.
        Priority: Environment Variables > .env file > config.yaml
        """
        return (
            env_settings,
            DotEnvSettingsSource(settings_cls, (base_dir / ".env")),
            YamlConfigSettingsSource(settings_cls, (base_dir / "config.yaml")),
        )


def get_settings():
    """
    Factory function to initialize settings and export API keys to the environment.
    This ensures that downstream libraries like LiteLLM can access the keys automatically.
    """
    settings = Settings()
    os.environ["ANTHROPIC_API_KEY"] = settings.anthropic.api_key
    os.environ["GEMINI_API_KEY"] = settings.gemini.api_key
    os.environ["OPENAI_API_KEY"] = settings.chatgpt.api_key
    return settings
