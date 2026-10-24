
import json
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
EVALS_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(APP_DIR))

from agent import run_agent
from evals.criteria_checker import check_criteria

GOLDEN_SET = EVALS_DIR / "golden_set.json"



def evaluate_case(test_case: dict) -> dict:
    test_id = test_case["id"]
    question = test_case["question"]
    criteria = test_case.get("required_criteria", [])

    print("\n" + "=" * 60)
    print("Test:", test_id)
    print("Question:", question)

    if not criteria:
        print("ERROR: No required_criteria defined.")
        return {"id": test_id, "passed": False}

    try:
        answer = run_agent(question)
        print("\nAnswer:", answer)

        result = check_criteria(answer, criteria)

        for index, matched in enumerate(
            result["criteria_results"], start=1
        ):
            if matched:
                print(f"  PASS Criterion {index}")
            else:
                print(f"  FAIL Criterion {index}")
                print("       Expected one of:", criteria[index - 1])

        print(
            f"Criteria passed: {result['criteria_passed']}/"
            f"{result['criteria_total']}"
        )

        status = result["passed"]
        print("Overall result:", "PASS" if status else "FAIL")

        return {
            "id": test_id,
            "passed": status,
            "criteria_passed": result["criteria_passed"],
            "criteria_total": result["criteria_total"],
        }

    except Exception as exc:
        print("ERROR:", str(exc))
        return {
            "id": test_id,
            "passed": False,
            "error": str(exc),
        }


def main():
    if not GOLDEN_SET.exists():
        print("ERROR: Golden set not found:", GOLDEN_SET)
        return

    try:
        test_cases = json.loads(
            GOLDEN_SET.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        print("ERROR: Invalid JSON:", exc)
        return

    if not isinstance(test_cases, list) or not test_cases:
        print("ERROR: Golden set must be a non-empty JSON list.")
        return

    results = [evaluate_case(case) for case in test_cases]

    passed = sum(result["passed"] for result in results)
    total = len(results)

    print("\n" + "=" * 60)
    print("FINAL EVALUATION REPORT")
    print(f"Tests passed: {passed}/{total}")
    print(f"Tests failed: {total - passed}/{total}")
    print(f"Pass rate: {passed / total * 100:.1f}%")

    print("\nTest breakdown:")
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"- {result['id']}: {status}")


if __name__ == "__main__":
    main()
