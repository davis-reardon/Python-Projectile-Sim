import csv
import subprocess
import sys


def load_requirements(filepath="requirements/requirements.csv"):
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def run_test(test_id):
    """
    Run a single named test via pytest -k, return True if it passed.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-k", test_id, "-q"],
        capture_output=True, text=True
    )
    return "1 passed" in result.stdout


def generate_traceability_matrix(requirements):
    matrix = []
    for req in requirements:
        passed = run_test(req["test_id"])
        matrix.append({
            "id": req["id"],
            "test_id": req["test_id"],
            "result": "Pass" if passed else "Fail",
        })
    return matrix


def print_matrix(matrix):
    print(f"{'Requirement':<15}{'Test':<55}{'Result'}")
    print("-" * 85)
    for row in matrix:
        print(f"{row['id']:<15}{row['test_id']:<55}{row['result']}")


if __name__ == "__main__":
    requirements = load_requirements()
    matrix = generate_traceability_matrix(requirements)
    print_matrix(matrix)