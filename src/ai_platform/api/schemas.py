"""
Pydantic schemas for the AI Platform API.
Ensures data validation and provides clear documentation for the API request bodies.
"""

from pydantic import BaseModel, Field


class Chat(BaseModel):
    """
    Schema for incoming chat and query requests.
    Includes a maximum length constraint to prevent extremely large payloads.
    """

    message: str = Field(
        ..., max_length=1050, description="The user prompt or question"
    )
