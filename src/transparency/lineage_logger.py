import json
import os
import datetime

class LineageLogger:
    def __init__(self, log_path="build-artifacts/lineage.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_event(self, event_type, data):
        """
        Logs an event to the lineage log.
        data should be a dict containing event-specific metadata.
        """
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": event_type,
            **data
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def log_mutation(self, generation, parent_hash, child_hash, fitness_delta, gas_consumed, tests_passed, tests_failed, reason):
        self.log_event("mutation", {
            "generation": generation,
            "parent_hash": parent_hash,
            "child_hash": child_hash,
            "fitness_delta": fitness_delta,
            "gas_consumed": gas_consumed,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "reason": reason
        })
