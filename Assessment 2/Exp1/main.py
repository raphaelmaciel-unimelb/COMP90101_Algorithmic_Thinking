import os
import sys

# Add the parent folder to the system path so Python can find module files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataGenerator import DataGenerator
from ExperimentRunner import ExperimentRunner

if __name__ == "__main__":
    generator = DataGenerator()
    runner = ExperimentRunner(generator)
    
    print("Running Experiment 1: Push-Only Performance Comparison...\n")
    
    sizes, heap_times, comp_times = runner.run_exp1_push_only()
    
    print("\n--- Benchmark Complete ---")
    print(f"{'N Elements':<12} | {'MaxHeap Time (s)':<18} | {'CompetitorArray Time (s)':<22}")
    print("-" * 60)
    for s, h, c in zip(sizes, heap_times, comp_times):
        print(f"{s:<12,d} | {h:<18.4f} | {c:<22.4f}")