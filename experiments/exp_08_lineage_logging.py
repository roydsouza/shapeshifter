import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from transparency.lineage_logger import LineageLogger

def test_lineage_logging():
    print("--- Testing Lineage Logging (Phase 5a) ---")
    log_path = "build-artifacts/test_lineage.jsonl"
    if os.path.exists(log_path):
        os.remove(log_path)
        
    logger = LineageLogger(log_path=log_path)
    
    logger.log_mutation(
        generation=1,
        parent_hash="abc",
        child_hash="def",
        fitness_delta=0.1,
        gas_consumed=50,
        tests_passed=3,
        tests_failed=0,
        reason="Optimization test"
    )
    
    assert os.path.exists(log_path)
    with open(log_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["event"] == "mutation"
        assert record["generation"] == 1
        assert record["parent_hash"] == "abc"
        
    print("Lineage Logging Verification Successful.")

if __name__ == "__main__":
    test_lineage_logging()
