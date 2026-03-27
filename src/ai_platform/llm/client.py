import anthropic
import uuid
from ai_platform.config import Settings
from ai_platform.logger import get_logger

logger = get_logger(__name__)


class AnthropicClient():
    def __init__(self,settings:Settings):
        self.api_key = settings.anthropic.api_key
        self.model = settings.anthropic.model
        self.max_tokens = settings.anthropic.max_tokens
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def send_message(self,message):
        
        try:
            request_id = uuid.uuid4()
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": message}]
            )
            total_tokens = response.usage.input_tokens + response.usage.output_tokens

            logger.info(f'request {request_id} used total of {total_tokens} tokens, input_tokens - {response.usage.input_tokens} and {response.usage.output_tokens} outtokens')

            return response.content[0].text

        except anthropic.RateLimitError as e:
            logger.warning(f'req id {request_id} {e}')
            raise 
        
        except anthropic.APIConnectionError as e:
            logger.warning(f'req id {request_id} {e}')
            raise 

        except anthropic.APIStatusError as e:
            if e.status_code in [500,529]:
                logger.error(f'req id {request_id} {e}')
                raise # retry methods - logs
            
            elif e.status_code in [400,402,404]:
                logger.error(f'req id {request_id} {e}')
                raise # print message - log 
            
            elif e.status_code in [401,403,413]:
                logger.error(f'req id {request_id} {e}')
                raise # print message - log

            else:
                logger.error(f'req id {request_id} {e}')
                raise 
