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
- `SCD-41.ino` - Arduino code that outputs `CO2,temperature,humidity` string every 5s to the its serial port
- `SCD-41.py` - Python code that reads data from the Arduino serial port and either
  - Prints the string to the console
  - Saves the data to Firebase Firestore if `s` flag is used. Specifically, `-s` saves using a Firestore collection name given by today's date e.g. `20240326` . Using `-s chicken` will save under a collection named e.g. `20240326-chicken`
