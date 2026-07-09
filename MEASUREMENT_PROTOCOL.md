# Energy Measurement Protocol

**SAI Framework — Energy Sustainability (Z Dimension)**  
**Version:** 0.2.1  
**Date:** July 2026

## Overview

This document provides detailed procedures for measuring energy consumption of LLM inference for the **Z dimension** of the SAI Framework.

SAI defines a **three-tier measurement system** to balance rigor with accessibility.

## Energy Scope (Normative)

`Total_Energy_Joules` used in `Z = Y / (Total_Energy_Joules × PUE)` MUST correspond to the **same evaluation suite** that produced Y.

| Approach | When to use |
|----------|-------------|
| Direct suite measurement | Preferred for Tier 1 when feasible |
| Probe + scale | Measure standardized probe (§Tier 1 config), derive J/token or phase rates, scale to suite tokens/timings; document method |
| Token × intensity | Tier 2: `Suite_Tokens × Energy_per_Token` with cited source |

A probe-only energy figure (e.g., one 2048→512 run) MUST NOT be used as `Total_Energy_Joules` without scaling to the suite.

## Three-Tier Measurement System

### Tier 1: Hardware Measurement (Highest Confidence)
- **Method:** Direct power measurement from GPU/CPU
- **Required for:** SAI-Full conformance
- **Confidence Level:** ±2% accuracy
- **Tools:** nvidia-smi, NVML API, TokenPowerBench, or equivalent

### Tier 2: API-Based Estimation (Medium Confidence)
- **Method:** Provider-reported token counts + published benchmarks
- **Required for:** SAI-Basic conformance (minimum)
- **Confidence Level:** ±10-15% accuracy
- **Sources:** ML.Energy leaderboard, academic papers, vendor documentation

### Tier 3: Literature-Based Estimation (Informational Only)
- **Method:** Published measurements from research papers
- **Use case:** Preliminary comparisons, model selection
- **Confidence Level:** ±20-30% accuracy
- **Not sufficient for formal SAI conformance**

## Tier 1: Hardware Measurement Protocol

### Required Hardware

**Minimum Configuration:**
- NVIDIA GPU with power monitoring support (Tesla, A100, H100, RTX 3090+)
- NVML-compatible driver (535.x or later recommended)
- Linux-based OS (Ubuntu 20.04+ or CentOS 8+)

**Recommended Configuration:**
- Dedicated measurement server (minimize background processes)
- Hardware power meters (e.g., WattsUp PRO, NVIDIA Jetson with INA3221)
- Temperature monitoring (GPU and ambient)
- Isolated network to prevent interference

### Software Tools

#### Option A: nvidia-smi (Basic)
```bash
# Real-time power monitoring
nvidia-smi --query-gpu=timestamp,power.draw,utilization.gpu,temperature.gpu \
           --format=csv -l 1 > power_log.csv
```

**Pros:** Built-in, no installation  
**Cons:** 1-second sampling, limited accuracy

#### Option B: NVML API (Recommended)
```python
import pynvml
import time

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

samples = []
for _ in range(1000):
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Convert mW to W
    samples.append(power)
    time.sleep(0.01)  # 100 Hz sampling

average_power = sum(samples) / len(samples)
```

**Pros:** High frequency (up to 100 Hz), programmatic control  
**Cons:** Requires Python library

#### Option C: TokenPowerBench (Most Comprehensive)
```bash
# Install TokenPowerBench
git clone https://github.com/foundation-model-stack/power-benchmarks
cd power-benchmarks
pip install -e .

# Run measurement
python -m tokenpowerbench \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --input-length 2048 \
    --output-length 512 \
    --num-runs 100 \
    --output results.json
```

**Pros:** Phase-aware, standardized protocol, JSON output  
**Cons:** Requires setup, may not support all models

### Measurement Procedure

#### Step 1: Environment Preparation

1. **Isolate the GPU:**
   ```bash
   # Stop other GPU processes
   sudo systemctl stop docker
   pkill -f "python.*inference"
   
   # Verify GPU is idle
   nvidia-smi
   ```

2. **Set GPU to maximum performance mode:**
   ```bash
   sudo nvidia-smi -pm 1  # Enable persistence mode
   sudo nvidia-smi -lgc 1410,1410  # Lock GPU clock (adjust for your GPU)
   ```

3. **Wait for thermal stabilization:**
   - Run idle measurement for 5 minutes
   - GPU temperature should stabilize (±2°C)

#### Step 2: Baseline Measurement

Measure idle power consumption:

```python
import pynvml
import time

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

baseline_samples = []
for _ in range(300):  # 3 seconds at 100 Hz
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
    baseline_samples.append(power)
    time.sleep(0.01)

baseline_power = sum(baseline_samples) / len(baseline_samples)
print(f"Baseline idle power: {baseline_power:.2f} W")
```

**Record this value** – it will be subtracted from active measurements.

#### Step 3: Inference Measurement

**Standardized Test Configuration:**
```yaml
test_config:
  input_context: 2048 tokens
  output_length: 512 tokens
  batch_size: 1
  temperature: 0.0
  num_runs: 100
  warmup_runs: 10
```

**Measurement script:**
```python
import time
import pynvml
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Prepare test prompt (2048 tokens)
test_prompt = "..." * 2048  # Replace with actual benchmark prompt

# Warmup
for _ in range(10):
    _ = model.generate(tokenizer.encode(test_prompt, return_tensors="pt"), max_new_tokens=512)

# Measurement runs
energy_samples = []
for run in range(100):
    power_samples = []
    
    # Start power monitoring thread
    monitoring = True
    def monitor_power():
        while monitoring:
            power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
            power_samples.append(power)
            time.sleep(0.01)
    
    import threading
    monitor_thread = threading.Thread(target=monitor_power)
    monitor_thread.start()
    
    # Run inference
    start_time = time.time()
    output = model.generate(
        tokenizer.encode(test_prompt, return_tensors="pt"),
        max_new_tokens=512,
        do_sample=False
    )
    end_time = time.time()
    
    # Stop monitoring
    monitoring = False
    monitor_thread.join()
    
    # Calculate energy
    duration = end_time - start_time
    avg_power = sum(power_samples) / len(power_samples) - baseline_power
    energy_joules = avg_power * duration
    energy_samples.append(energy_joules)
    
    print(f"Run {run+1}: {energy_joules:.2f} J, {duration:.2f}s, {avg_power:.2f}W")

# Report statistics
import statistics
mean_energy = statistics.mean(energy_samples)
std_energy = statistics.stdev(energy_samples)
print(f"\nTotal Energy: {mean_energy:.2f} ± {std_energy:.2f} J (100 runs)")
```

#### Step 4: Phase-Aware Measurement (Advanced)

For SAI-Full conformance, separate prefill and decode phases:

```
Prefill_Energy = Power_prefill (W) × Time_prefill (s)
Decode_Energy  = Power_decode (W) × Time_decode (s)
Total_Energy   = Prefill_Energy + Decode_Energy
```

`Time_decode` is wall-clock decode duration (or Tokens × time_per_token). Do **not** multiply average power by both token count and total decode time.

```python
# Prefill: power samples during prompt processing only
prefill_energy = mean(prefill_power_w) * prefill_duration_s

# Decode: power samples during generation only
decode_energy = mean(decode_power_w) * decode_duration_s

total_energy = prefill_energy + decode_energy
print(f"Prefill: {prefill_energy:.2f} J, Decode: {decode_energy:.2f} J")
```

#### Step 5: PUE Application

Apply Power Usage Effectiveness multiplier:

```python
# Measured or default PUE
pue = 1.3  # Cloud deployment
total_energy_with_pue = total_energy * pue

print(f"Total Energy (with PUE {pue}): {total_energy_with_pue:.2f} J")
```

### Validation Checklist

Before submitting Tier 1 measurements:

- [ ] GPU clock locked to prevent throttling
- [ ] Thermal stability confirmed (±2°C for 5 minutes)
- [ ] Baseline idle power measured and subtracted
- [ ] Minimum 100 inference runs completed
- [ ] Power sampling rate ≥10 Hz (preferably 100 Hz)
- [ ] Warmup runs (10+) excluded from measurements
- [ ] Standard test configuration used (2048 input, 512 output)
- [ ] PUE documented (measured or default)
- [ ] Phase-aware breakdown provided (for SAI-Full)

### Expected Ranges (Sanity Check)

**NVIDIA A100 80GB:**
- Idle power: 50-80 W
- Inference power: 250-400 W (depends on model size)
- Energy per token: 10-50 J for 7B models, 50-200 J for 70B models

**NVIDIA RTX 4090:**
- Idle power: 20-40 W
- Inference power: 200-350 W
- Energy per token: 15-60 J for 7B models

If measurements fall significantly outside these ranges, verify setup.

## Tier 2: API-Based Estimation

When hardware measurement is not feasible, estimate energy using published benchmarks.

### Procedure

#### Step 1: Obtain Token Counts

Record token consumption from the inference provider's usage metadata (e.g., `prompt_tokens`, `completion_tokens`, `total_tokens` in API responses). Token counts must come from actual evaluation runs, not estimates.

```yaml
# Example usage record from a provider response
usage:
  prompt_tokens: 1024
  completion_tokens: 512
  total_tokens: 1536
```

#### Step 2: Find Energy Benchmark

Consult published sources:

**ML.Energy Leaderboard:**
- URL: https://ml.energy/leaderboard
- Provides: Energy per token (J/token) for popular models
- Example: Llama-3.1-8B = 0.15 J/token (approximate)

**Academic Papers:**
- Search Google Scholar for "[Model Name] energy consumption"
- Look for papers with GPU-specific measurements

**Vendor Documentation:**
- Some providers publish energy metrics (e.g., Hugging Face Model Cards)

#### Step 3: Calculate Energy

```python
# Example: Llama-3.1-8B from ML.Energy
energy_per_token = 0.15  # J/token (cite source!)

total_energy = total_tokens * energy_per_token
print(f"Estimated energy: {total_energy:.2f} J")
print(f"Source: ML.Energy Leaderboard, accessed July 2026")
```

#### Step 4: Apply PUE

```python
pue = 1.3  # Assume cloud deployment
total_energy_with_pue = total_energy * pue
```

### Tier 2 Requirements

- [ ] Token counts from actual API responses (not estimated)
- [ ] Energy benchmark source cited with date
- [ ] Benchmark hardware matches deployment (or documented difference)
- [ ] PUE assumption documented
- [ ] Confidence interval estimated: ±10-15%

### Tier 2 Limitations

**Acknowledge in methodology:**
- Energy benchmarks may use different hardware configurations
- Batch size, sequence length variations affect accuracy
- Prefill/decode phases not separated
- Model optimizations (quantization, flash attention) not always reflected

## Tier 3: Literature-Based Estimation

Use published research for preliminary comparisons.

### Sources

1. **Academic Papers:** arXiv, ACL Anthology, NeurIPS proceedings
2. **Technical Reports:** OpenAI, Anthropic, Meta model cards
3. **Industry Benchmarks:** MLPerf Inference, TPCx-AI

### Example

From hypothetical paper:
> "GPT-3.5-turbo consumes approximately 2.5 kWh per million tokens on NVIDIA A100."

```python
tokens = 145_000  # Your evaluation
energy_per_million_tokens = 2.5 * 3_600_000  # Convert kWh to J
energy = (tokens / 1_000_000) * energy_per_million_tokens
print(f"Estimated energy: {energy:.2f} J")
print(f"Source: [Paper citation]")
```

### Tier 3 Limitations

- **Not acceptable for SAI conformance** (Basic or Full)
- Informational only
- High uncertainty (±20-30%)
- Use for model selection, not certification

## Multi-GPU and Distributed Inference

For models requiring multiple GPUs:

```python
# Sum power across all GPUs
total_power = 0
for gpu_id in range(num_gpus):
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
    total_power += power
```

**PUE considerations:**
- Higher for distributed setups (networking overhead)
- Measure or use PUE = 1.5 for multi-node

## Carbon Intensity (Optional)

Convert energy to carbon emissions:

### Step 1: Determine Grid Intensity

**Real-time sources:**
- ElectricityMap API: `https://api.electricitymap.org/v3/carbon-intensity/latest?zone=US-CAL-CISO`
- WattTime API (US)

**Static sources:**
- EPA eGRID (US regional averages)
- IEA Emissions Factors database
- Default: 475 gCO2/kWh (global average, 2025)

### Step 2: Calculate Emissions

```python
energy_kwh = total_energy_joules / 3_600_000
grid_intensity = 400  # gCO2/kWh (example: California)
carbon_cost = energy_kwh * grid_intensity

print(f"Carbon emissions: {carbon_cost:.2f} gCO2")
```

### Reporting

Include in evaluation report:
```yaml
carbon_footprint:
  energy_kwh: 0.0451
  grid_intensity: 400
  grid_intensity_source: "ElectricityMap API, us-california, 2026-07-07"
  total_gco2: 18.04
  equivalent: "Charging 1.5 smartphones"
```

## Troubleshooting

### Issue: High variance in measurements
**Solution:** 
- Increase number of runs (200+)
- Verify GPU clock is locked
- Check for thermal throttling

### Issue: Power readings seem too low
**Solution:**
- Verify baseline subtraction is correct
- Check GPU is actually being used (not CPU fallback)
- Ensure model loaded on GPU (`model.to("cuda")`)

### Issue: Phase separation unclear
**Solution:**
- Use profiling tools (NVIDIA Nsight, PyTorch Profiler)
- Instrument code with manual timers
- Consider Tier 2 if phase-aware measurement impractical

## Reporting Template

```yaml
energy_measurement:
  tier: 1  # or 2, 3
  
  # Tier 1 only
  hardware:
    gpu: "NVIDIA A100 80GB SXM4"
    driver: "535.104.05"
    cuda: "12.1"
  measurement:
    tool: "NVML API via pynvml"
    sampling_rate: 100  # Hz
    num_runs: 100
    baseline_power: 65.3  # W
  
  # All tiers
  results:
    total_energy: 12500  # J
    pue: 1.3
    total_energy_with_pue: 16250  # J
    confidence: "±2%"  # Tier 1: ±2%, Tier 2: ±10-15%, Tier 3: ±20-30%
  
  # Optional
  phase_breakdown:
    prefill_energy: 3200  # J
    decode_energy: 9300  # J
  
  # Optional
  carbon:
    grid_intensity: 400  # gCO2/kWh
    total_gco2: 18.04
    source: "ElectricityMap API"
```

## References

- TokenPowerBench: https://github.com/foundation-model-stack/power-benchmarks
- ML.Energy Leaderboard: https://ml.energy/leaderboard
- NVIDIA Management Library (NVML): https://developer.nvidia.com/nvidia-management-library-nvml
- ElectricityMap API: https://www.electricitymap.org/
- Green Software Foundation: https://greensoftware.foundation/

---

**For questions or contributions to this protocol, please open an issue on the SAI Framework repository.**
