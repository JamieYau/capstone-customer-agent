from pydantic import BaseModel, Field

class IntentResult(BaseModel):
    intent: str = Field(description="Detected intent")
    order_id: str | None = Field(default=None)
