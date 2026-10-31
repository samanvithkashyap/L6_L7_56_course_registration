import pytest

from course_registration import can_register, late_fee, waitlist_position


@pytest.mark.parametrize(
    ("status", "current", "course", "prerequisites", "expected"),
    [
        ("regular", 20, 4, True, "registered"),
        ("probation", 16, 1, True, "credit limit exceeded"),
        ("honors", 28, 1, True, "credit limit exceeded"),
        ("regular", 20, 4, False, "prerequisites missing"),
    ],
)
def test_can_register_decision_branches(
    status, current, course, prerequisites, expected
):
    assert can_register(status, current, course, prerequisites) == expected


def test_can_register_boundary_and_error_branches():
    assert can_register("regular", 23, 1, True) == "registered"
    assert can_register("regular", 24, 1, True) == "credit limit exceeded"

    with pytest.raises(ValueError, match="unknown status"):
        can_register("unknown", 0, 1, True)

    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, -1, True)


@pytest.mark.parametrize(
    ("enrolled", "capacity", "length", "expected"),
    [
        (0, 1, 0, 0),
        (1, 1, 0, 1),
        (1, 1, 9, 10),
        (1, 1, 10, -1),
    ],
)
def test_waitlist_decision_branches(enrolled, capacity, length, expected):
    assert waitlist_position(enrolled, capacity, length) == expected


def test_waitlist_capacity_error_branch():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, -1, 0)


@pytest.mark.parametrize(
    ("days_late", "credits", "waiver", "expected"),
    [
        (0, 21, False, 0),
        (-1, 1, False, 0),
        (1, 20, True, 0),
        (1, 20, False, 500),
        (7, 20, False, 500),
        (8, 20, False, 600),
        (8, 21, False, 850),
        (25, 21, False, 2000),
        (26, 21, False, 2000),
    ],
)
def test_late_fee_decision_branches(days_late, credits, waiver, expected):
    assert late_fee(days_late, credits, waiver) == expected
