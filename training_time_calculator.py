# Configuration
NUM_TOKENS_BILLIONS = 1000  # For 1 Trillion tokens
FLOPS_PER_PARAMETER_PER_TOKEN = 6

# GPU Data: GPU_name -> Dense BF16/FP16 TFLOPs
GPU_DATA = {
    'A100_PCIE_80GB': 312,
    'H100_NVL_PCIE': 835.5,
    'H800_PCIE': 835.5,  # Assumed same as H100 NVL/PCIe
    'B200_SXM_PER_GPU': 2250,
}

# Model Data: Model_name/size -> Parameters (Billions)
MODEL_DATA = {
    '7B': 7,
    '17B': 17,
    '32B': 32,
    '320B': 320,
    '671B': 671,
}

def calculate_and_print_training_times():
    """
    Calculates and prints the estimated training time for LLMs on different GPUs.
    """
    for gpu_name, gpu_tflops in GPU_DATA.items():
        print(f"\nCalculations for GPU: {gpu_name}")
        print("-" * (20 + len(gpu_name)))
        print(f"{'Model Size':<12} | {'Parameters (B)':<15} | {'Est. Training Time (Hours)':<28} | {'Est. Training Time (Days)':<25}")
        print("-" * 90)

        for model_size_str, model_params_B in MODEL_DATA.items():
            # Calculate total FLOPs required for training
            # total_flops = FLOPs/param/token * num_params * num_tokens
            total_flops = FLOPS_PER_PARAMETER_PER_TOKEN * model_params_B * (10**9) * NUM_TOKENS_BILLIONS * (10**9)

            # Calculate time in seconds
            # time_seconds = total_flops / (gpu_tflops_per_second)
            # gpu_tflops_per_second is gpu_tflops * 10^12
            if gpu_tflops == 0:
                time_seconds = float('inf') # Avoid division by zero
            else:
                time_seconds = total_flops / (gpu_tflops * (10**12))

            # Convert time to hours and days
            time_hours = time_seconds / 3600
            time_days = time_hours / 24

            print(f"{model_size_str:<12} | {model_params_B:<15} | {time_hours:<28.2f} | {time_days:<25.2f}")
        print("-" * 90)

    print("\nNote: These calculations are based on theoretical peak FLOPs (dense, non-sparse BF16/FP16 precision)")
    print("and assume 100% Model FLOPs Utilization (MFU). Actual training times can be 1.5x to 3x longer")
    print("(i.e., MFU of 33-66%) due to factors like software overhead, interconnect bottlenecks, specific model")
    print("architecture, and batch sizes. The default calculation is for 1 Trillion tokens.")

if __name__ == "__main__":
    calculate_and_print_training_times()
