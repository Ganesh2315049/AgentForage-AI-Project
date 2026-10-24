
from criteria_checker import check_criteria


def test_correct_answer_passes():
    answer = "Event ID 4625 indicates a failed logon attempt."
    criteria = [
        ["failed logon", "failed authentication"]
    ]

    result = check_criteria(answer, criteria)

    assert result["passed"] is True


def test_missing_criterion_fails():
    answer = "Event ID 4625 is a Windows security event."
    criteria = [
        ["failed logon", "failed authentication"]
    ]

    result = check_criteria(answer, criteria)

    assert result["passed"] is False


def test_all_required_criteria_must_match():
    answer = "Repeated failed logins do not prove an attack."
    criteria = [
        ["do not prove", "does not prove"],
        ["additional evidence", "contextual evidence"],
    ]

    result = check_criteria(answer, criteria)

    assert result["passed"] is False
    assert result["criteria_passed"] == 1
    assert result["criteria_total"] == 2


def test_negated_answer_fails():
    answer = "Event ID 4625 does not indicate a failed logon."
    criteria = [
        ["failed logon", "failed authentication"]
    ]

    result = check_criteria(answer, criteria)

    assert result["passed"] is False


def test_empty_criteria_do_not_pass():
    answer = "Any answer"
    criteria = []

    result = check_criteria(answer, criteria)

    assert result["passed"] is False
    assert result["criteria_total"] == 0
