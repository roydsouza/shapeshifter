import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from transparency.regression_sentinel import RegressionSentinel

def test_regression_sentinel():
    print("--- Testing Regression Sentinel (Phase 5c) ---")
    
    # We'll use a mock test command that we can control
    sentinel = RegressionSentinel(test_command=["true"]) # 'true' always exits 0
    
    state = {"applied": False}
    
    def apply_fn(): state["applied"] = True
    def rollback_fn(): state["applied"] = False
    
    # Test Pass case
    passed, out = sentinel.verify_variant(apply_fn, rollback_fn)
    assert passed is True
    assert state["applied"] is True
    print("Sentinel PASS verification successful.")
    
    # Test Fail case
    sentinel.test_command = ["false"] # 'false' always exits 1
    passed, out = sentinel.verify_variant(apply_fn, rollback_fn)
    assert passed is False
    assert state["applied"] is False # Should have rolled back
    print("Sentinel FAIL/ROLLBACK verification successful.")

if __name__ == "__main__":
    test_regression_sentinel()
