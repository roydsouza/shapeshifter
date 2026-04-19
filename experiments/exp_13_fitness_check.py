import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from interpreter import ShapeshifterInterpreter

def main():
    interp = ShapeshifterInterpreter()
    
    # Define the fitness functions as Python S-expressions (as used in mirror_lib.lisp)
    interp.evaluate(['defn', 'calculate-fitness', ['correctness', 'speed-ratio', 'gas-ratio'],
        ['mul', 'correctness', ['add', ['mul', 0.5, 'speed-ratio'], ['mul', 0.5, 'gas-ratio']]]])
    
    interp.evaluate(['defn', 'score-variant', ['metrics', 'baseline-metrics', 'correctness'],
        ['begin',
            ['defn', 'get-avg', ['m', 'key'], ['dict-get', ['dict-get', 'm', 'key'], 'avg']],
            ['defn', 'get-count', ['m', 'key'], ['dict-get', ['dict-get', 'm', 'key'], 'count']],
            ['defn', 'speed-ratio', [], ['div', ['get-avg', 'baseline-metrics', 'call.op.add'], ['get-avg', 'metrics', 'call.op.add']]],
            ['defn', 'gas-ratio', [], ['div', ['get-count', 'baseline-metrics', 'op.add'], ['get-count', 'metrics', 'op.add']]],
            ['calculate-fitness', 'correctness', ['speed-ratio'], ['gas-ratio']]
        ]
    ])

    # Baseline: speed=1.0, gas=1.0
    baseline = {
        'call.op.add': {'avg': 100},
        'op.add': {'count': 10}
    }
    
    # Scenario A: 2x Speed, 2x Efficiency (Gas=5), 100% Correct
    # Calculation: C=1.0 * (0.5 * 2.0 + 0.5 * 2.0) = 2.0
    metrics_a = {
        'call.op.add': {'avg': 50},
        'op.add': {'count': 5}
    }
    
    # Scenario B: 4x Speed, 0% Correct
    # Calculation: C=0.0 * (0.5 * 4.0 + 0.5* 2.0) = 0.0
    metrics_b = {
        'call.op.add': {'avg': 25},
        'op.add': {'count': 5}
    }

    print("Experiment 13: Fitness Function Verification")
    print("-" * 40)
    
    score_a = interp.evaluate(['score-variant', metrics_a, baseline, 1.0])
    print(f"Scenario A (Improvement): Expected ~2.0, Got {score_a}")
    
    score_b = interp.evaluate(['score-variant', metrics_b, baseline, 0.0])
    print(f"Scenario B (Regression):  Expected 0.0, Got {score_b}")

    if score_a > 1.0 and score_b == 0.0:
        print("\nSUCCESS: Fitness Function Logic Verified.")
    else:
        print("\nFAILURE: Fitness Function Logic Inconsistent.")

if __name__ == "__main__":
    main()
