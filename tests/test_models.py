from app.schemas import ModelResponseBase, Priority, Category
from pydantic import ValidationError
import pytest


def test_valid_model_response():
    model = ModelResponseBase.model_validate_json('{"priority": "medium", "category": "refund", "safety_risk": false, "needs_clarification": false}')

    assert model.priority == Priority.MEDIUM
    assert model.category == Category.REFUND
    assert model.safety_risk is False
    assert model.needs_clarification is False

def test_invalid_priority():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json('{"priority": "urgent", "category": "refund", "safety_risk": false, "needs_clarification": false}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "enum"
    assert errors[0]["loc"] == ('priority',)

def test_missing_field():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json(
            '{"category": "refund", "safety_risk": false, "needs_clarification": false}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert errors[0]["loc"] == ('priority',)

def test_safety_risk_rejects_string():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json(
            '{"priority": "medium", "category": "refund", "safety_risk": "no", "needs_clarification": false}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "bool_type"
    assert errors[0]["loc"] == ('safety_risk',)

def test_additional_field():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json(
            '{"priority": "medium", "category": "refund", "safety_risk": false, "needs_clarification": false, "description": "Hello!"}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "extra_forbidden"
    assert errors[0]["loc"] == ('description',)

def test_invalid_category_field():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json(
            '{"priority": "medium", "category": "buying", "safety_risk": false, "needs_clarification": false}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "enum"
    assert errors[0]["loc"] == ('category',)

def test_malformed_json():
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json('This is your json formatted pydantic scheme: "priority": "medium", "category": "buying", "safety_risk": false, "needs_clarification": false}')

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["type"] == "json_invalid"
    assert errors[0]["loc"] == ()

@pytest.mark.parametrize('priority,safety_risk', [
    (Priority.MEDIUM, True),
    (Priority.LOW, True)
])
def test_safety_risk_with_low_priority(priority, safety_risk):
    with pytest.raises(ValidationError) as exc_info:
        ModelResponseBase.model_validate_json(
            '{"priority": "low", "category": "refund", "safety_risk": true, "needs_clarification": false}'
        )

    errors = exc_info.value.errors()
    print(errors)
    assert len(errors) == 1
    assert errors[0]["type"] == "value_error"
    assert errors[0]["loc"] == ()