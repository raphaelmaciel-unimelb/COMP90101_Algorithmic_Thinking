import time
import matplotlib.pyplot as plt
from DataGenerator import DataGenerator
from MaxHeap import MaxHeap
from CompetitorArray import CompetitorArray

class ExperimentRunner:
    def __init__(self, generator):
        self.generator = generator

    def run_exp1_push_only(self, sizes=[10000, 50000, 100000, 500000, 1000000]):
        """Runs N push operations for both data structures and records timings."""
        heap_times = []
        comp_times = []

        for N in sizes:
            script = self.generator.gen_exp1_sequence(N)

            # Benchmark MaxHeap
            heap = MaxHeap()
            start = time.perf_counter()
            for op in script:
                heap.push(op[1])
            heap_times.append(time.perf_counter() - start)

            # Benchmark CompetitorArray
            comp = CompetitorArray()
            start = time.perf_counter()
            for op in script:
                comp.push(op[1])
            comp_times.append(time.perf_counter() - start)

        self.plot_exp1(sizes, heap_times, comp_times)
        return sizes, heap_times, comp_times

    def plot_exp1(self, sizes, heap_times, comp_times):
        """Generates and saves the performance chart for Experiment 1."""
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap (O(N log N))')
        plt.plot(sizes, comp_times, marker='s', color='orange', linewidth=2, label='CompetitorArray (O(N))')

        plt.title('Experiment 1: Push-Only Performance Comparison', fontsize=14)
        plt.xlabel('Number of Elements (N)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        
        # Save high-res figure for your GitHub repo & academic report
        plt.savefig('experiment1_push_only.png', dpi=300)
        plt.show()

    def run_exp2_gettop_ratio(self, total_ops=100000, percentages=[0, 20, 40, 60, 80, 95]):
        """Experiment 2: Measures total time across varying getTop() percentages."""
        heap_times = []
        comp_times = []

        for pct in percentages:
            script = self.generator.gen_exp2_sequence(total_ops, pct)

            # Benchmark MaxHeap
            heap = MaxHeap()
            start = time.perf_counter()
            for item in script:
                op = item[0] if isinstance(item, (tuple, list)) else item
                val = item[1] if isinstance(item, (tuple, list)) and len(item) > 1 else None

                if op == 1:
                    heap.push(val)
                elif op == 2:
                    heap.pop()
                elif op == 3:
                    heap.getTop()
            heap_times.append(time.perf_counter() - start)

            # Benchmark CompetitorArray
            comp = CompetitorArray()
            start = time.perf_counter()
            for item in script:
                op = item[0] if isinstance(item, (tuple, list)) else item
                val = item[1] if isinstance(item, (tuple, list)) and len(item) > 1 else None

                if op == 1:
                    comp.push(val)
                elif op == 2:
                    comp.pop()
                elif op == 3:
                    comp.getTop()
            comp_times.append(time.perf_counter() - start)

        self.plot_exp2(percentages, heap_times, comp_times, total_ops)
        return percentages, heap_times, comp_times

    def plot_exp2(self, percentages, heap_times, comp_times, total_ops):
        """Generates and saves the performance chart for Experiment 2."""
        plt.figure(figsize=(10, 6))
        plt.plot(percentages, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap')
        plt.plot(percentages, comp_times, marker='s', color='orange', linewidth=2, label='CompetitorArray')

        plt.title(f'Experiment 2: Execution Time vs. getTop() Ratio ({total_ops:,} Operations)', fontsize=14)
        plt.xlabel('Percentage of getTop() Operations (%)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()

        plt.savefig('experiment2_gettop_ratio.png', dpi=300)
        plt.show()

    def run_exp3_pop_ratio(self, total_ops=50000, percentages=[0, 10, 20, 30, 40, 50]):
        """Experiment 3: Measures total time across varying pop() percentages."""
        heap_times = []
        comp_times = []

        for pct in percentages:
            script = self.generator.gen_exp3_sequence(total_ops=total_ops, pop_pct=pct)

            # Benchmark MaxHeap
            heap = MaxHeap()
            start = time.perf_counter()
            for item in script:
                op, val = item[0], item[1]
                if op == 1:
                    heap.push(val)
                elif op == 2:
                    heap.pop()
            heap_times.append(time.perf_counter() - start)

            # Benchmark CompetitorArray
            comp = CompetitorArray()
            start = time.perf_counter()
            for item in script:
                op, val = item[0], item[1]
                if op == 1:
                    comp.push(val)
                elif op == 2:
                    comp.pop()
            comp_times.append(time.perf_counter() - start)

        self.plot_exp3(percentages, heap_times, comp_times, total_ops)
        return percentages, heap_times, comp_times

    def plot_exp3(self, percentages, heap_times, comp_times, total_ops):
        """Generates and saves the performance chart for Experiment 3."""
        plt.figure(figsize=(10, 6))
        plt.plot(percentages, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap (O(log N) pop)')
        plt.plot(percentages, comp_times, marker='s', color='orange', linewidth=2, label='CompetitorArray (O(N) pop)')

        plt.title(f'Experiment 3: Execution Time vs. pop() Ratio ({total_ops:,} Operations)', fontsize=14)
        plt.xlabel('Percentage of pop() Operations (%)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()

        plt.savefig('experiment3_pop_ratio.png', dpi=300)
        plt.show()
    
    def run_exp4_heapify_vs_push(self, sizes=[10000, 50000, 100000, 500000, 1000000, 2000000]):
        """Experiment 4: Compares O(N) heapify vs N * O(log N) sequential pushes."""
        push_times = []
        heapify_times = []

        for N in sizes:
            data = self.generator.gen_exp4_list(N)

            # 1. Sequential Push-All (O(N log N))
            heap_push = MaxHeap()
            start = time.perf_counter()
            for val in data:
                heap_push.push(val)
            push_times.append(time.perf_counter() - start)

            # 2. Floyd's Heapify (O(N))
            heap_build = MaxHeap()
            start = time.perf_counter()
            heap_build.heapify(data)
            heapify_times.append(time.perf_counter() - start)

        self.plot_exp4(sizes, push_times, heapify_times)
        return sizes, push_times, heapify_times

    def plot_exp4(self, sizes, push_times, heapify_times):
        """Generates and saves the performance chart for Experiment 4."""
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, push_times, marker='o', color='purple', linewidth=2, label='Sequential Push (O(N log N))')
        plt.plot(sizes, heapify_times, marker='s', color='green', linewidth=2, label="Floyd's Heapify (O(N))")

        plt.title("Experiment 4: Sequential Push vs. Floyd's Heapify Construction", fontsize=14)
        plt.xlabel('Number of Elements (N)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()

        plt.savefig('experiment4_heapify_vs_push.png', dpi=300)
        plt.show()