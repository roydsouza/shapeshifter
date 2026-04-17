import subprocess

class RegressionSentinel:
    def __init__(self, test_command=["python3", "-m", "pytest"]):
        self.test_command = test_command

    def run_tests(self):
        """
        Runs the test suite. Returns True if all tests pass.
        """
        print(f"\n[SENTINEL] Running regression tests: {' '.join(self.test_command)}...")
        try:
            result = subprocess.run(self.test_command, capture_output=True, text=True)
            if result.returncode == 0:
                print("[SENTINEL] Tests PASSED.")
                return True, result.stdout
            else:
                print("[SENTINEL] Tests FAILED.")
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def verify_variant(self, apply_fn, rollback_fn):
        """
        Applies a mutation, runs tests, and rolls back if they fail.
        """
        apply_fn()
        passed, output = self.run_tests()
        if not passed:
            print("[SENTINEL] REGRESSION DETECTED. Rolling back...")
            rollback_fn()
            return False, output
        return True, output
