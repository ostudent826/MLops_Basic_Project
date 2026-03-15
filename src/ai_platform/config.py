from pathlib import Path
from pydantic_settings import BaseSettings, YamlConfigSettingsSource

base_dir = Path(__file__).parent.parent.parent

#creating setting validator
class Settings(BaseSettings):
        log_level: str = 'info'
        api_url: str
        api_timeout: int
        max_retries: int
        backoff_multiplier: int

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
            YamlConfigSettingsSource(settings_cls, (base_dir / "config.yaml"))
        )

