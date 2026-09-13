import time
import gc
import matplotlib.pyplot as plt
from DataGenerator import DataGenerator
from MaxHeap import MaxHeap
from CompetitorArray import CompetitorArray

TIMEOUT_SECONDS = 3 * 3600  # 3 Hours limit per specification

class ExperimentRunner:
    """Sequential runner complying with sequence reuse and timeout specifications."""

    def __init__(self, generator: DataGenerator):
        self.generator = generator

    # --- EXPERIMENT 1 ---
    def run_exp1_push_only(self, sizes=[100_000, 200_000, 500_000, 800_000, 1_000_000]):
        print("=== Starting Experiment 1: Push-Only Workload ===", flush=True)
        heap_times, comp_times = [], []
        saved_sequences = {}  # Store sequences for Experiment 4 reuse

        for N in sizes:
            print(f"\n[Exp 1] Generating sequence for N = {N:,}...", flush=True)
            script = self.generator.gen_exp1_sequence(N)
            saved_sequences[N] = script  # Save for Exp 4

            # 1. MaxHeap
            gc.disable()
            heap = MaxHeap()
            t0 = time.perf_counter()
            for _, val in script:
                heap.push(val)
            t_heap = time.perf_counter() - t0
            gc.enable()
            heap_times.append(t_heap)

            # 2. CompetitorArray
            gc.disable()
            comp = CompetitorArray()
            t0 = time.perf_counter()
            for _, val in script:
                comp.push(val)
            t_comp = time.perf_counter() - t0
            gc.enable()
            comp_times.append(t_comp)

            print(f"  └ Complete [N = {N:,}] -> Heap: {t_heap:.4f}s | Competitor: {t_comp:.4f}s", flush=True)

        self.plot_exp1(sizes, heap_times, comp_times)
        return saved_sequences

    # --- EXPERIMENT 2 ---
    def run_exp2_gettop_ratio(self, total_ops=1_000_000, percentages=[0.1, 0.5, 1.0, 5.0, 10.0]):
        print("\n=== Starting Experiment 2: Execution Time vs. getTop() Ratio ===", flush=True)
        heap_times, comp_times = [], []

        for pct in percentages:
            print(f"\n[Exp 2] Generating sequence for getTop = {pct}% ({total_ops:,} ops)...", flush=True)
            script = self.generator.gen_exp2_sequence(total_ops=total_ops, gettop_pct=pct)

            # 1. MaxHeap
            gc.disable()
            heap = MaxHeap()
            t0 = time.perf_counter()
            for op, val in script:
                if op == 1: heap.push(val)
                elif op == 3: heap.getTop()
            t_heap = time.perf_counter() - t0
            gc.enable()
            heap_times.append(t_heap)

            # 2. CompetitorArray
            gc.disable()
            comp = CompetitorArray()
            t0 = time.perf_counter()
            for op, val in script:
                if op == 1: comp.push(val)
                elif op == 3: comp.getTop()
            t_comp = time.perf_counter() - t0
            gc.enable()
            comp_times.append(t_comp)

            print(f"  └ Complete [getTop = {pct}%] -> Heap: {t_heap:.4f}s | Competitor: {t_comp:.4f}s", flush=True)

        self.plot_exp2(percentages, heap_times, comp_times, total_ops)

    # --- EXPERIMENT 3 ---
    def run_exp3_pop_ratio(self, total_ops=1_000_000, percentages=[0.1, 0.5, 1.0, 5.0, 10.0]):
        print("\n=== Starting Experiment 3: Execution Time vs. pop() Ratio ===", flush=True)
        heap_times, comp_times = [], []

        for pct in percentages:
            print(f"\n[Exp 3] Generating sequence for pop = {pct}% ({total_ops:,} ops)...", flush=True)
            script = self.generator.gen_exp3_sequence(total_ops=total_ops, pop_pct=pct)

            # 1. MaxHeap
            gc.disable()
            heap = MaxHeap()
            t0 = time.perf_counter()
            for op, val in script:
                if op == 1: heap.push(val)
                elif op == 2: heap.pop()
            t_heap = time.perf_counter() - t0
            gc.enable()
            heap_times.append(t_heap)

            # 2. CompetitorArray (Progress Monitored with Timeout Guard)
            gc.disable()
            comp = CompetitorArray()
            t0 = time.perf_counter()
            timed_out = False

            for idx, (op, val) in enumerate(script, start=1):
                if op == 1: comp.push(val)
                elif op == 2: comp.pop()

                if idx % 250_000 == 0:
                    elapsed = time.perf_counter() - t0
                    print(f"  ├ Competitor Progress: {idx:,}/{total_ops:,} ops ({(idx/total_ops)*100:.0f}%) | Elapsed: {elapsed:.1f}s", flush=True)
                    if elapsed > TIMEOUT_SECONDS:
                        print("  └ [TERMINATED] Exceeded 3-hour limit (Out of Time)", flush=True)
                        comp_times.append("Out of Time")
                        timed_out = True
                        break

            gc.enable()
            if not timed_out:
                t_comp = time.perf_counter() - t0
                comp_times.append(t_comp)
                print(f"  └ Complete [pop = {pct}%] -> Heap: {t_heap:.4f}s | Competitor: {t_comp:.4f}s", flush=True)

        self.plot_exp3(percentages, heap_times, comp_times, total_ops)

    # --- EXPERIMENT 4 ---
    def run_exp4_heapify_vs_push(self, saved_sequences):
        """Reuses the exact push-only sequences sigma_1 ... sigma_5 generated in Experiment 1."""
        print("\n=== Starting Experiment 4: Batch Construction (Heapify vs Push-One-By-One) ===", flush=True)
        push_times, heapify_times = [], []
        sizes = list(saved_sequences.keys())

        for N in sizes:
            script = saved_sequences[N]  # REUSE exact sequence from Exp 1

            # Method 1: Heapify
            gc.disable()
            heap_build = MaxHeap()
            t0 = time.perf_counter()
            elements = [val for _, val in script]
            heap_build.heapify(elements)
            t_heapify = time.perf_counter() - t0
            gc.enable()
            heapify_times.append(t_heapify)

            # Method 2: Sequential Push
            gc.disable()
            heap_push = MaxHeap()
            t0 = time.perf_counter()
            for _, val in script:
                heap_push.push(val)
            t_push = time.perf_counter() - t0
            gc.enable()
            push_times.append(t_push)

            speedup = t_push / t_heapify if t_heapify > 0 else 0
            print(f"  └ Complete [N = {N:,}] -> Heapify: {t_heapify:.4f}s | Push: {t_push:.4f}s | Speedup: {speedup:.2f}x", flush=True)

        self.plot_exp4(sizes, push_times, heapify_times)

    # --- PLOTTING METHODS ---
    def plot_exp1(self, sizes, heap_times, comp_times):
        plt.figure(figsize=(9, 5.5))
        plt.plot(sizes, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap')
        plt.plot(sizes, comp_times, marker='s', color='orange', linewidth=2, label='CompetitorArray')
        plt.title('Experiment 1: Time vs Length of Push-Only Sequence', fontsize=13, fontweight='bold')
        plt.xlabel('Sequence Length (L)', fontsize=11)
        plt.ylabel('Overall Running Time (seconds)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('experiment1_push_only.png', dpi=300)
        plt.close()

    def plot_exp2(self, percentages, heap_times, comp_times, total_ops):
        plt.figure(figsize=(9, 5.5))
        plt.plot(percentages, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap')
        plt.plot(percentages, comp_times, marker='s', color='orange', linewidth=2, label='CompetitorArray')
        plt.title(f'Experiment 2: Time vs getTop Percentage (L = {total_ops:,})', fontsize=13, fontweight='bold')
        plt.xlabel('getTop Percentage (%)', fontsize=11)
        plt.ylabel('Overall Running Time (seconds)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('experiment2_gettop_ratio.png', dpi=300)
        plt.close()

    def plot_exp3(self, percentages, heap_times, comp_times, total_ops):
        # Filter out 'Out of Time' string entries for clean numeric plotting
        valid_comp = [t for t in comp_times if isinstance(t, (int, float))]
        valid_pcts = percentages[:len(valid_comp)]

        plt.figure(figsize=(9, 5.5))
        plt.plot(percentages, heap_times, marker='o', color='blue', linewidth=2, label='MaxHeap')
        plt.plot(valid_pcts, valid_comp, marker='s', color='orange', linewidth=2, label='CompetitorArray')
        plt.title(f'Experiment 3: Time vs pop Percentage (L = {total_ops:,})', fontsize=13, fontweight='bold')
        plt.xlabel('pop Percentage (%)', fontsize=11)
        plt.ylabel('Overall Running Time (seconds)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('experiment3_pop_ratio.png', dpi=300)
        plt.close()

    def plot_exp4(self, sizes, push_times, heapify_times):
        plt.figure(figsize=(9, 5.5))
        plt.plot(sizes, push_times, marker='o', color='purple', linewidth=2, label='push-one-by-one')
        plt.plot(sizes, heapify_times, marker='s', color='green', linewidth=2, label='heapify')
        plt.title('Experiment 4: Heapify vs Push-One-By-One Construction', fontsize=13, fontweight='bold')
        plt.xlabel('Sequence Length (L)', fontsize=11)
        plt.ylabel('Overall Running Time (seconds)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('experiment4_heapify_vs_push.png', dpi=300)
        plt.close()