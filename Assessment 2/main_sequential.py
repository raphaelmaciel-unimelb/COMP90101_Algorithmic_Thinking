from DataGenerator import DataGenerator
from ExperimentRunner import ExperimentRunner

if __name__ == "__main__":
    generator = DataGenerator()
    runner = ExperimentRunner(generator)

    # 1. Run Exp 1 and capture the 5 push-only sequences sigma_1 ... sigma_5
    saved_sequences = runner.run_exp1_push_only()

    # 2. Run Exp 2
    runner.run_exp2_gettop_ratio()

    # 3. Run Exp 3
    runner.run_exp3_pop_ratio()

    # 4. Run Exp 4 passing the saved sequences from Exp 1
    runner.run_exp4_heapify_vs_push(saved_sequences)

    print("\n=========================================")
    print(" ALL EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("=========================================")