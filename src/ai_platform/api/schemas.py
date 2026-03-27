from pydantic import BaseModel, Field

class Chat(BaseModel):
    message: str = Field(max_length=1050)