# BrainFlow Overview

**Docs:** https://brainflow.readthedocs.io/en/stable/index.html

BrainFlow is an open-source library (MIT) that handles EEG data acquisition AND signal processing in one unified Python API. It natively supports OpenBCI Cyton, which means we can replace the `openbci-python` approach in `Control_Template.py` with BrainFlow and get a lot of calibration/processing work for free.

```
pip install brainflow
```

---

## What We Get For Free

### Board Connection (replaces openbci-python)

```python
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

params = BrainFlowInputParams()
params.serial_port = 'COM3'  # or '/dev/ttyUSB0' on Linux/Mac

board = BoardShim(BoardIds.CYTON_BOARD, params)
board.prepare_stream()
board.start_stream()

data = board.get_board_data()  # 2D array: rows = channels, cols = samples
eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_BOARD)
```

### Signal Filtering (no manual math needed)

```python
from brainflow.data_filter import DataFilter, FilterTypes

# Clean up noise on a channel
DataFilter.perform_bandpass(data[ch], sampling_rate=250, start_freq=1.0, stop_freq=50.0, ...)
DataFilter.perform_bandstop(data[ch], sampling_rate=250, start_freq=58.0, stop_freq=62.0, ...)  # 60Hz notch
```

### Band Power Analysis (key for directional intent)

```python
# Returns average and std dev of band powers across channels
# Bands: delta, theta, alpha, beta, gamma
avg_bands, std_bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate=250, apply_filters=True)
```

Alpha and beta band power are the most relevant for motor imagery (thinking about movement):
- **Alpha suppression** (8–12 Hz) over motor cortex = movement intent
- **Beta band** (12–30 Hz) changes correlate with left/right motor planning

### Built-in Mental State Classifiers

BrainFlow ships two pre-trained Logistic Regression classifiers:
- **Concentration metric** — useful as an activation threshold
- **Relaxation metric** — useful for idle/rest state detection

These can serve as a baseline gate: only process directional commands when concentration is above a threshold.

---

## What We Still Need to Build

BrainFlow does **not** include directional/motor imagery classifiers — that's the custom piece:

| Task | Status |
|---|---|
| Board connection & raw data | ✅ BrainFlow handles |
| Noise filtering | ✅ BrainFlow handles |
| Band power extraction | ✅ BrainFlow handles |
| Concentration/relaxation state | ✅ BrainFlow handles |
| Directional intent (left/right/up/down) | 🔨 We build with labeled data |
| Mouse movement | ✅ pynput handles |

---

## Revised Integration Plan

1. Use `BoardShim` to connect to Cyton and stream data
2. Use `DataFilter.get_avg_band_powers()` to extract alpha/beta features per channel
3. Record labeled calibration samples for each direction
4. Train a simple classifier (scikit-learn → export as ONNX for BrainFlow compatibility)
5. Load classifier back into BrainFlow's MLModel or run it directly in Python
6. Map output to `pynput` mouse commands

BrainFlow supports loading custom ONNX models (scikit-learn via `skl2onnx`, TensorFlow via `tf2onnx`), so the full pipeline can stay within the BrainFlow ecosystem.
