# Sensirion SCD-41

- Measures
  - CO2
  - Temperature
  - Humidity
- Available to buy from [AdaFruit](https://www.adafruit.com/product/5190)
- [Resources and technical specifications](https://sensirion.com/products/catalog/SCD41/)
- [Arduino code snippets](https://github.com/Sensirion/arduino-snippets)
- [Sensirion Arduino library](https://github.com/Sensirion/arduino-i2c-scd4x/tree/master)

This folder contains two files that are designed to work together
- `SCD-41.ino` - Arduino code that outputs `OK,CO2,temperature,humidity` every ~5s to its serial port
- `SCD-41.py` - Python code that reads data from the Arduino serial port and either
  - Prints the string to the console
  - Saves the data to Firebase Firestore if `s` flag is used. Specifically, `-s` saves using a Firestore collection name given by today's date e.g. `20240326` . Using `-s chicken` will save under a collection named e.g. `20240326-chicken`

## Requirements / setup (Arduino + Raspberry Pi)

### Hardware
- Raspberry Pi (tested with: Raspberry Pi 3) connected to the Arduino over USB
- Arduino connected to the SCD-41 over I2C (SDA/SCL + power + ground)
  - If you’re using an Arduino Uno: SDA = A4, SCL = A5

### Arduino (upload the sketch)
1. Install the Arduino IDE (or `arduino-cli`).
2. Install the Sensirion library `SensirionI2CScd4x` (Arduino Library Manager: “Sensirion I2C SCD4x”).
3. Open `SCD-41.ino` and upload it to your board.
4. Verify the Arduino is outputting a line like `OK,500,23.4,45.6` every ~5 seconds at `115200` baud.

### Raspberry Pi (run the Python reader)
From this folder: `cd SCD-41`

Install OS packages:
- `sudo apt update`
- `sudo apt install -y python3 python3-venv curl`

Install `uv` (recommended):
- `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your shell (or ensure `~/.local/bin` is on your `PATH`) and confirm: `uv --version`
- Other install options: https://docs.astral.sh/uv/getting-started/installation/

Install Python dependencies + run (no manual venv activation):
- `uv sync`
- `uv run SCD-41.py`

Notes:
- `uv sync` will create `.venv/` and `uv.lock` in this folder (you do not need to activate the venv manually).

Serial port permissions:
- Permanent fix: add your user to `dialout` (then log out/in or reboot): `sudo usermod -a -G dialout $USER`
- Verify your user has the group: `groups $USER`
- Verify the device is owned by `dialout`: `ls -l /dev/ttyACM0` (or your device path)
- Find which device the Arduino is using: `ls -l /dev/serial/by-id/` (preferred) or `ls /dev/ttyACM* /dev/ttyUSB*`
- If it’s not `/dev/ttyACM0`, update the port in `SCD-41.py` (look for `serial.Serial(...)`).

### Required local files (gitignored)
`SCD-41.py` expects these files next to it:
- `key.json` - Firebase service account key used by `firebase-admin` / Firestore
- `config.py` - must define `TARGET_URL = "https://..."` for the HTTP PUT call

If you don’t want to use Firebase or the HTTP PUT, the script will need to be adjusted (right now it imports/initializes both unconditionally).

### Run
- Print readings: `uv run SCD-41.py`
- Save to Firestore: `uv run SCD-41.py -s` or `uv run SCD-41.py -s some-suffix`
- Stop: press `Esc` (keyboard listener) or `Ctrl+C`
