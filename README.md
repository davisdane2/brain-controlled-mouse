# brain-controlled-mouse

A Python proof-of-concept for translating brain-computer interface (BCI) signals into mouse control. EEG brainwave data is classified and sent as directional commands via USB, which are then used to move the system mouse in real time.

## Hardware/Software

- Windows 11 PC w/ USB or be on same Wi-Fi Network
- **[OpenBCI GUI Software](https://docs.openbci.com/Software/OpenBCISoftware/GUIDocs/#download-the-standalone-app)** - Windows 11 GUI Software to work with device.
- **[OpenBCI Cyton](https://docs.openbci.com/Software/SoftwareLanding/)** — an 8-channel EEG board that streams raw brainwave data to a computer via USB dongle (serial at 115,200 baud).
- **[OpenBCI Documentation](https://docs.openbci.com)** - Main Documentation page for more info to program signals.
## How It Works

1. OpenBCI Cyton streams raw 24-bit EEG samples at 250 Hz over USB serial
2. **[BrainFlow](https://brainflow.readthedocs.io/en/stable/index.html)** (`pip install brainflow`) handles board connection, noise filtering, and band power extraction out of the box
3. Alpha/beta band power features per channel are fed into a custom directional classifier (`left`, `right`, `up`, `down`)
4. Commands are passed to `pynput` to move the system mouse

See `Brainflow_Calibration/Overview.md` for details on what BrainFlow provides vs. what we build.

## Roadmap - Control a YouTube Video (Left,Right,Up,Down, Play, Pause, Next)

### Phase 1 — Data Collection ✅
- Record mouse movement data (`mouse_log.csv`)
- Label movement data for classifier training (`mouse_log_labeled.csv`)

### Phase 2 — Proof of Concept (Current)
- [ ] Find/Download/Install Drivers for Wi-fi or USB connection of openBCI EEG device and make sure signals can be collected by OS.
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
