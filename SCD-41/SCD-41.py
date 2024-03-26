import time
import datetime
import argparse
import serial
from pynput import keyboard

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Create an argument parser
parser = argparse.ArgumentParser(description='Environmental monitoring')

# Add the desired command line flag
parser.add_argument('-s', '--save', nargs='?', const=True, default=False, 
                    help='Save sensor output to firebase. Optionally provide suffix for the firebase collection.')

# Parse the command line arguments
args = parser.parse_args()

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Generate today's date in the format YYYYMMDD
today_str = datetime.datetime.now().strftime("%Y%m%d")

# Check if a save is requested
if args.save is not False:
    # If `args.save` is True, it means '-s' flag was used without a specific filename
    if args.save is True:
        # The data will be saved in a collection whose name is today's date
        data_label = today_str  
    else:
        # The data will be saved in a collection whose name is today's date with a suffix provided by the user
        # e.g. 20240326-chicken if user runs the program using "-s chicken"
        data_label = f"{today_str}-{args.save}"
    doc_ref = db.collection(data_label).document('0')
    doc_ref.set({
        u'CO2': 0,
        u'Temperature': 0,
        u'Humidity': 0
    }, merge=True)

else:
    print("Not saving the output.")


# Allows user to stop the program gracefully using esc
stop_program = False
def on_keypress(key):
    global stop_program
    if key == keyboard.Key.esc:
        print("Escape key pressed. Exiting...")
        stop_program = True
        return False

# Create a keyboard listener
listener = keyboard.Listener(on_press=on_keypress)
# Start listening for key presses
listener.start()

ser = serial.Serial('/dev/ttyACM0', 115200)

while not stop_program:
    # Converts bytes into a string, interpreting the bytes as text according to a 
    # specific encoding (UTF-8 by default). Strips new line characters.
    s = ser.readline().decode().strip()

    # Formats data into an array
    data = s.split(',')

    # Checks that the data is in the expected format
    if (len(data) == 4) & (data[0] == "OK"):
        try:
            co2 = float(data[1])
            temperature = float(data[2])
            humidity = float(data[3])
            now = str(round(time.time()))
            print(f'Time: {now}, CO2: {co2} ppm, Temperature: {temperature} C, Humidity: {humidity} %')
            if args.save:
                doc_ref = db.collection(data_label).document(now)
                doc_ref.set({
                    u'CO2': co2,
                    u'Temperature': temperature,
                    u'Humidity': humidity
                }, merge=True)
        except Exception as e:
            print("corrupt data")
            print(e)
    else:
        print("corrupt data")