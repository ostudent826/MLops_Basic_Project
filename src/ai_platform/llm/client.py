import anthropic
import logging
import uuid
from ai_platform.config import Settings



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

            logging.info(f'request {request_id} used total of {total_tokens} tokens, input_tokens - {response.usage.input_tokens} and {response.usage.output_tokens} outtokens')

            return response.content[0].text

        except anthropic.RateLimitError as e:
            logging.warning(f'req id {request_id} {e}')
            raise 
        
        except anthropic.APIConnectionError as e:
            logging.warning(f'req id {request_id} {e}')
            raise 

        except anthropic.APIStatusError as e:
            if e.status_code in [500,529]:
                logging.error(f'req id {request_id} {e}')
                raise # retry methods - logs
            
            elif e.status_code in [400,402,404]:
                logging.error(f'req id {request_id} {e}')
                raise # print message - log 
            
            elif e.status_code in [401,403,413]:
                logging.error(f'req id {request_id} {e}')
                raise # print message - log

            else:
                logging.error(f'req id {request_id} {e}')
                raise 
