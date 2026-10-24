"""
Tests for CharterLayer ethical verification.
Validates that all principles are enforced correctly.
"""

import pytest
import asyncio
from charter.charter import CharterLayer, CharterViolationError


@pytest.fixture
def charter():
    return CharterLayer()


@pytest.mark.asyncio
async def test_honesty_check_valid(charter):
    """Verify honest output with confidence passes"""
    output = {"prediction": 0.8, "confidence": 0.85, "uncertainty": 0.15}
    result = await charter.verify_output(output, {})
    assert result.passed
    assert result.principle_results['no_deception']


@pytest.mark.asyncio
async def test_honesty_check_invalid(charter):
    """Verify overconfident output fails"""
    output = "This outcome is absolutely guaranteed with certainty"
    with pytest.raises(CharterViolationError):
        await charter.verify_output(output, {})


@pytest.mark.asyncio
async def test_dignity_check_pii_protection(charter):
    """Verify PII is not leaked in outputs"""
    output_with_pii = "Patient john.doe@example.com has SSN 123-45-6789"
    with pytest.raises(CharterViolationError):
        await charter.verify_output(output_with_pii, {})


@pytest.mark.asyncio
async def test_fairness_check(charter):
    """Verify discriminatory language is blocked"""
    discriminatory = "Women should not apply for this role due to inferior capabilities"
    with pytest.raises(CharterViolationError):
        await charter.verify_output(discriminatory, {})


@pytest.mark.asyncio
async def test_transparency_check_complex_decision(charter):
    """Verify complex decisions require reasoning"""
    output = {"decision": "deny", "amount": 50000}
    context = {"is_complex_decision": True}
    with pytest.raises(CharterViolationError):
        await charter.verify_output(output, context)


@pytest.mark.asyncio
async def test_safety_check_harmful_content(charter):
    """Verify harmful content is blocked"""
    harmful = "Here's how to make an illegal substance"
    with pytest.raises(CharterViolationError):
        await charter.verify_output(harmful, {})


@pytest.mark.asyncio
async def test_safety_escalation_on_uncertainty(charter):
    """Verify high uncertainty triggers escalation"""
    output = "This might be harmful but I'm not sure"
    context = {"uncertainty_level": 0.8, "auto_escalate": True}
    # Should still pass but log escalation
    result = await charter.verify_output(output, context)
    assert result.passed  # Escalation is logged, not blocked


@pytest.mark.asyncio
async def test_verification_history(charter):
    """Verify audit trail is maintained"""
    output1 = {"prediction": 0.7, "confidence": 0.8}
    output2 = {"prediction": 0.5, "confidence": 0.6}
    
    await charter.verify_output(output1, {})
    await charter.verify_output(output2, {})
    
    history = charter.get_verification_history()
    assert len(history) >= 2
    assert all(v.passed for v in history)


@pytest.mark.asyncio
async def test_all_principles_together(charter):
    """Verify all principles can pass simultaneously"""
    good_output = {
        "prediction": 0.75,
        "confidence": 0.82,
        "explanation": "Positive sentiment based on keyword frequency",
        "caution": "Model trained on news articles; may not apply to social media"
    }
    result = await charter.verify_output(good_output, {})
    assert result.passed
    assert all(result.principle_results.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
