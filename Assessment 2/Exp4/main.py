import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataGenerator import DataGenerator
from ExperimentRunner import ExperimentRunner

if __name__ == "__main__":
    generator = DataGenerator()
    runner = ExperimentRunner(generator)

    print("Running Experiment 4: Floyd's Heapify vs. Sequential Push...\n")

    sizes, push_times, heapify_times = runner.run_exp4_heapify_vs_push(
        sizes=[10000, 50000, 100000, 500000, 1000000, 2000000]
    )

    print("\n--- Benchmark Complete ---")
    print(f"{'N Elements':<12} | {'Sequential Push (s)':<20} | {'Floyd Heapify (s)':<18}")
    print("-" * 58)
    for s, p, h in zip(sizes, push_times, heapify_times):
        print(f"{s:<12,d} | {p:<20.4f} | {h:<18.4f}")