from pathlib import Path
from pydantic_settings import BaseSettings, YamlConfigSettingsSource, SettingsConfigDict, DotEnvSettingsSource
from pydantic import BaseModel

base_dir = Path(__file__).parent.parent.parent


class AnthropicSettings(BaseModel):
    api_key: str
    model: str = "anthropic/claude-haiku-4-5"

class GeminiSettings(BaseModel):
    api_key: str
    model: str = "gemini/gemini-2.5-flash"

class ChatgptSettings(BaseModel):
    api_key: str
    model: str = "openai/gpt-4o-mini"

#creating setting validator
class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file=base_dir / ".env",
            env_file_encoding= "utf-8",
            env_nested_delimiter="__"

        )
        environment: str = "dev"
        log_level: str = 'info'
        api_url: str
        api_timeout: int
        max_retries: int
        backoff_multiplier: int
        anthropic:AnthropicSettings
        gemini:GeminiSettings
        chatgpt:ChatgptSettings
        max_user_token: int
        max_tokens: int = 10000

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls,
            init_settings,                    
            env_settings,                     
            dotenv_settings,      
            file_secret_settings, 
        ) :  
            return(
            env_settings,
            DotEnvSettingsSource(settings_cls, (base_dir / ".env")),
            YamlConfigSettingsSource(settings_cls, (base_dir / "config.yaml"))
        )

def get_settings():
    settings = Settings()
    return settings