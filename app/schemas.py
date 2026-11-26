from pydantic import BaseModel
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
    priority: Priority
    category: Category
    safety_risk: bool
    needs_clarification: bool