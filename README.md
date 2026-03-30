# brain-controlled-mouse

A Python proof-of-concept for translating brain-computer interface (BCI) signals into mouse control. EEG brainwave data is classified and sent as directional commands via USB, which are then used to move the system mouse in real time.

## Hardware

**[OpenBCI Cyton](https://docs.openbci.com/Software/SoftwareLanding/)** — an 8-channel EEG board that streams raw brainwave data to a computer via USB dongle (serial at 115,200 baud).

## How It Works

1. OpenBCI Cyton streams raw 24-bit EEG samples at 250 Hz over USB serial
2. A Python script reads the stream via the `openbci-python` library (`pip install openbci-python`)
3. Each `OpenBCISample` contains 8 channels of raw voltage data — scaled to microvolts using the board's gain factor
4. A trained classifier maps EEG signal patterns to directional commands (`left`, `right`, `up`, `down`)
5. Commands are passed to `pynput` or `pyautogui` to move the system mouse

## Roadmap

### Phase 1 — Data Collection ✅
- Record mouse movement data (`mouse_log.csv`)
- Label movement data for classifier training (`mouse_log_labeled.csv`)

### Phase 2 — Proof of Concept (Current)
- [ ] Connect to OpenBCI Cyton via `openbci-python` and stream raw samples
- [ ] Identify and isolate EEG channels/features that correspond to directional intent
- [ ] Calibration routine: record stable baseline signals for `left`, `right`, `up`, `down`
- [ ] Mouse control script: map calibrated commands to movement via `pynput`/`pyautogui`

### Phase 3 — Classifier Integration
- [ ] Train movement classifier on labeled EEG data
- [ ] Replace calibration-based thresholds with real-time classifier output
- [ ] Tune movement sensitivity and response latency

### Phase 4 — Full BCI Pipeline
- [ ] End-to-end: OpenBCI headset → classifier → mouse control
- [ ] Click support
- [ ] Configurable movement speed and step size
