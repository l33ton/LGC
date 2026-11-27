from pydantic import BaseModel, ConfigDict, model_validator, ValidationError
from enum import StrEnum

class Priority(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
class Category(StrEnum):
    DELIVERY = "delivery"
    REFUND = "refund"
    BUSINESS_RELATED = "business-related"

class ModelResponseBase(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    priority: Priority
    category: Category
    safety_risk: bool
    needs_clarification: bool

    @model_validator(mode='after')
    def check_safety_risk_and_priority(self):
        if self.safety_risk == True and self.priority != Priority.HIGH:
            raise ValueError("Safety risk must be with HIGH priority")
        return self


