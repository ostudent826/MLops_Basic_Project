import yaml
import os
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent

with open(base_dir / 'config.yaml', 'r') as file:
    config = yaml.safe_load(file)


LOG_LEVEL          = os.environ.get('LOG_LEVEL', config.get('log_level'))
API_TIMEOUT        = int(os.environ.get('API_TIMEOUT', config.get('api_timeout')))
API_URL            = os.environ.get('API_URL', config.get('api_url'))
MAX_RETRIES        = int(os.environ.get('MAX_RETRIES', config.get('max_retries')))
BACKOFF_MULTIPLIER = int(os.environ.get('BACKOFF_MULTIPLIER', config.get('backoff_multiplier')))

