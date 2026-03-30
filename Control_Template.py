"""
Control_Template.py

Template for reading OpenBCI Cyton EEG data and mapping classified signals
to mouse movement. Intended as a starting point — calibration and classifier
logic are left as placeholders.

Requirements:
    pip install openbci-python pynput
"""

import openbci
from pynput.mouse import Controller

# --- Configuration ---
SERIAL_PORT = None        # Set to port string (e.g. '/dev/ttyUSB0') or None to auto-detect
MOVE_STEP = 20            # Pixels to move per command

mouse = Controller()

# --- Classifier Placeholder ---
def classify(sample):
    """
    Takes an OpenBCISample and returns a direction string or None.

    Replace this with your trained classifier or calibration-based thresholds.

    Args:
        sample: OpenBCISample with .channels_data (list of 8 voltage readings)

    Returns:
        One of 'left', 'right', 'up', 'down', or None
    """
    # Example stub — replace with real signal logic
    return None


# --- Mouse Control ---
def move_mouse(direction):
    if direction == 'left':
        mouse.move(-MOVE_STEP, 0)
    elif direction == 'right':
        mouse.move(MOVE_STEP, 0)
    elif direction == 'up':
        mouse.move(0, -MOVE_STEP)
    elif direction == 'down':
        mouse.move(0, MOVE_STEP)


# --- Sample Callback ---
def handle_sample(sample):
    direction = classify(sample)
    if direction:
        print(f"Command: {direction}")
        move_mouse(direction)


# --- Main ---
if __name__ == '__main__':
    print("Connecting to OpenBCI Cyton...")
    board = openbci.Cyton(port=SERIAL_PORT)

    print("Streaming — press Ctrl+C to stop.")
    try:
        board.start_stream(handle_sample)
    except KeyboardInterrupt:
        board.stop_stream()
        print("Stopped.")
