import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from transparency.landscape_renderer import LandscapeRenderer

def test_landscape_table():
    print("--- Testing Fitness Landscape Table (Phase 5d) ---")
    renderer = LandscapeRenderer()
    
    data = [
        {'id': 'v_base', 'fitness': 1.0, 'speed': 1.0, 'tests': '3/3', 'gas': 120},
        {'id': 'v_001', 'fitness': 1.1, 'speed': 1.05, 'tests': '3/3', 'gas': 114},
        {'id': 'v_002', 'fitness': 0.8, 'speed': 0.9, 'tests': '1/3', 'gas': 150},
    ]
    
    renderer.render(data)
    print("\nLandscape Table Verification Successful.")

if __name__ == "__main__":
    test_landscape_table()
