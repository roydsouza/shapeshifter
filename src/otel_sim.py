import time
from collections import defaultdict

class OTelSim:
    def __init__(self):
        # Store metrics as: {metric_name: [list_of_values]}
        self.metrics = defaultdict(list)
        # Store counts separately for easy access
        self.counts = defaultdict(int)

    def record_value(self, name, value):
        self.metrics[name].append(value)
        self.counts[name] += 1

    def increment(self, name, amount=1):
        self.counts[name] += amount

    def get_summary(self):
        summary = {}
        for name, values in self.metrics.items():
            if values:
                summary[name] = {
                    'avg': sum(values) / len(values),
                    'count': len(values),
                    'max': max(values),
                    'min': min(values)
                }
        
        # Add simple counters
        for name, count in self.counts.items():
            if name not in summary:
                summary[name] = {'count': count}
            else:
                summary[name]['total_count'] = count
                
        return summary

# Global singleton for the experiment
otel = OTelSim()
