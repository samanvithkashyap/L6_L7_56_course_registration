import pytest

from course_registration import can_register, late_fee, waitlist_position


def test_can_register_success_and_credit_limit():
    assert can_register("regular", 20, 4, True) == "registered"
    assert can_register("honors", 28, 1, True) == "credit limit exceeded"


def test_can_register_validation_and_prerequisites():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("guest", 0, 3, True)

    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, 0, True)

    assert can_register("probation", 8, 4, False) == "prerequisites missing"


def test_waitlist_position_outcomes():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)

    assert waitlist_position(30, 40, 0) == 0
    assert waitlist_position(40, 40, 2) == 3
    assert waitlist_position(40, 40, 10) == -1


def test_late_fee_outcomes():
    assert late_fee(0, 10, False) == 0
    assert late_fee(5, 10, True) == 0
    assert late_fee(5, 10, False) == 500
    assert late_fee(10, 10, False) == 800
    assert late_fee(10, 24, False) == 1050
    assert late_fee(30, 24, False) == 2000
