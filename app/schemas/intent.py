from pydantic import BaseModel, Field
from typing import Literal, Optional

class IntentResult(BaseModel):
    intent: Literal["order_tracking", "faq", "policy", "unknown"]
    confidence: Literal["low", "medium", "high"]
    order_id: Optional[str] = Field(
        default=None,
        description="Order ID if user intent is order_tracking"
    )
