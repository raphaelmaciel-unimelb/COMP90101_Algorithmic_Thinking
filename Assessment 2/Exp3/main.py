import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataGenerator import DataGenerator
from ExperimentRunner import ExperimentRunner

if __name__ == "__main__":
    generator = DataGenerator()
    runner = ExperimentRunner(generator)

    print("Running Experiment 3: Time vs. pop% Ratio...\n")

    percentages, heap_times, comp_times = runner.run_exp3_pop_ratio(
        total_ops=50000, 
        percentages=[0, 10, 20, 30, 40, 50]
    )

    print("\n--- Benchmark Complete ---")
    print(f"{'pop %':<10} | {'MaxHeap Time (s)':<18} | {'CompetitorArray Time (s)':<22}")
    print("-" * 58)
    for p, h, c in zip(percentages, heap_times, comp_times):
        print(f"{p:<10}% | {h:<18.4f} | {c:<22.4f}")