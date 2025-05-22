document.addEventListener('DOMContentLoaded', () => {
    const FLOPS_PER_PARAMETER_PER_TOKEN = 6;

    const gpuSelect = document.getElementById('gpu-select');
    const modelParamsInput = document.getElementById('modelParams');
    const numTokensInput = document.getElementById('numTokens');
    const calculateBtn = document.getElementById('calculateBtn');
    const resultHoursDisplay = document.getElementById('resultHours');
    const resultDaysDisplay = document.getElementById('resultDays');

    calculateBtn.addEventListener('click', () => {
        const gpuTflopsStr = gpuSelect.value;
        const modelParamsStr = modelParamsInput.value;
        const numTokensStr = numTokensInput.value;

        // Input Validation
        if (!gpuTflopsStr) {
            alert("请选择一个GPU型号。");
            return;
        }

        const modelParamsB = parseFloat(modelParamsStr);
        if (isNaN(modelParamsB) || modelParamsB <= 0) {
            alert("请输入有效的模型参数数量（必须是正数）。");
            modelParamsInput.focus();
            return;
        }

        const numTokensB = parseFloat(numTokensStr);
        if (isNaN(numTokensB) || numTokensB <= 0) {
            alert("请输入有效的训练Token数量（必须是正数）。");
            numTokensInput.focus();
            return;
        }

        const gpuTflops = parseFloat(gpuTflopsStr);
        if (isNaN(gpuTflops) || gpuTflops === 0) {
            alert("选择的GPU TFLOPs无效，无法计算。");
            return;
        }

        // Calculation Logic
        // total_flops = FLOPs/param/token * num_params * num_tokens
        const totalFlops = FLOPS_PER_PARAMETER_PER_TOKEN * modelParamsB * 1e9 * numTokensB * 1e9;

        // time_seconds = total_flops / (gpu_tflops_per_second)
        // gpu_tflops_per_second is gpu_tflops * 10^12
        const timeSeconds = totalFlops / (gpuTflops * 1e12);

        const timeHours = timeSeconds / 3600;
        const timeDays = timeHours / 24;

        // Display Results
        resultHoursDisplay.textContent = `预估训练时间（小时）：${timeHours.toFixed(2)}`;
        resultDaysDisplay.textContent = `预估训练时间（天）：${timeDays.toFixed(2)}`;
    });
});
