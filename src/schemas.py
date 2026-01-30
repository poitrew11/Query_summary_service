from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    result: bool = Field()


class SummaryInput(BaseModel):
    request_id: str = Field(..., description="Request ID of the task")
    chat_id: str = Field(..., description="UUID representing the chat session")
    user_id: int = Field(..., description="Unique identifier for the user")
    question: str = Field(..., description="The user's input question or message")


class SummaryOutput(BaseModel):
    request_id: str = Field(..., description="Request ID of the task")
    chat_id: str = Field(..., description="UUID representing the chat session")
    user_id: int = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="The output summary")
