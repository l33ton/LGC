from app.schemas import ModelResponseBase, Priority
from pydantic import ValidationError
import pytest


def test_valid_priority():
    model_response = ModelResponseBase(priority="medium", category="refund", safety_risk=False, needs_clarification=False) #type: ignore

    assert model_response.priority == Priority.MEDIUM

def test_invalid_priority():
    with pytest.raises(ValidationError):
        ModelResponseBase(priority="urgent", category="refund", safety_risk=False, needs_clarification=False) #type: ignore

def test_missing_field():
    with pytest.raises(ValidationError):
        ModelResponseBase(priority="medium", category="refund", needs_clarification=False) #type: ignore  

def test_invalid_field():
    with pytest.raises(ValidationError):
        ModelResponseBase(priority="medium", category="refund", safety_risk="no", needs_clarification=False) #type: ignore    

def test_additional_field():
    with pytest.raises(ValidationError):
        ModelResponseBase(priority="medium", category="refund", safety_risk=False, needs_clarification=False, description= "DDOS Attack") #type: ignore
