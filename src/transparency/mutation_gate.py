import os
import sys

class MutationGate:
    def __init__(self, pending_dir="pending_mutations"):
        self.pending_dir = pending_dir
        os.makedirs(self.pending_dir, exist_ok=True)

    def stage_mutation(self, current_code, proposed_code, diff, evidence, gas_cost):
        """
        Stages a mutation for human review.
        Returns True if forward, False if vetoed.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.md"
        path = os.path.join(self.pending_dir, filename)

        with open(path, "w") as f:
            f.write(f"# Pending Mutation: {timestamp}\n\n")
            f.write(f"## Evidence\n{evidence}\n\n")
            f.write(f"## Gas Cost\n{gas_cost} steps\n\n")
            f.write(f"## Proposed Change\n```diff\n{diff}\n```\n")

        print(f"\n[MUTATION STAGED] See {path}")
        print("Type 'forward' to apply or 'veto' to discard.")
        
        while True:
            choice = input("> ").strip().lower()
            if choice == "forward":
                return True
            if choice == "veto":
                return False
            print("Invalid input. Type 'forward' or 'veto'.")

import datetime # Fix missing import in template
