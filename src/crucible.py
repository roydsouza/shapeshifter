import sys
from pathlib import Path
from interpreter import ShapeshifterInterpreter

def render_landscape(interp, baseline, variants):
    """Renders a landscape table by evaluating the DSL 'score-variant' function."""
    print("\nFitness Landscape Snapshot (DSL Evaluated)")
    print("-" * 64)
    print(f"{'Variant':<12} | {'Fitness':<8} | {'Speed':<8} | {'Steps':<8} | {'Tests':<8}")
    print("-" * 64)
    
    for v in variants:
        try:
            fitness = interp.evaluate(['score-variant', v['metrics'], baseline, v['correctness']])
            speed_ratio = baseline['call.op.add']['avg'] / v['metrics']['call.op.add']['avg']
            print(f"{v['name']:<12} | {fitness:<8.2f} | {speed_ratio:<8.2f} | {v['metrics']['op.add']['count']:<8} | {int(v['correctness']*100)}%")
        except Exception as e:
            print(f"{v['name']:<12} | ERROR: {e}")
    print("-" * 64)

def main():
    interp = ShapeshifterInterpreter()
    interp.enable_mirror_mode()
    
    # Load DSL Logic (Nervous System)
    # For PoC, we manually inject the score-variant function as used in exp_13
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

    print("[CRUCIBLE] Mirror Reviewer Bridge initialized.")
    
    # Handshake Check
    try:
        if interp.evaluate(['mirror-exists', 'build-artifacts/mirror_handshake.txt']):
            print("[CRUCIBLE] Bridge Controller: Handshake verified.")
            
            # Demonstration of render_landscape
            baseline = {'call.op.add': {'avg': 100}, 'op.add': {'count': 10}}
            variants = [
                {'name': 'variant-001', 'metrics': {'call.op.add': {'avg': 50}, 'op.add': {'count': 5}}, 'correctness': 1.0},
                {'name': 'variant-002', 'metrics': {'call.op.add': {'avg': 20}, 'op.add': {'count': 5}}, 'correctness': 0.0}
            ]
            render_landscape(interp, baseline, variants)
        else:
            print("[CRUCIBLE] Bridge Controller: WARNING - Handshake missing.")
    except Exception as e:
        print(f"[CRUCIBLE] Bridge failure: {e}")

if __name__ == "__main__":
    main()
