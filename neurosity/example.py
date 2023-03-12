from neurosity import neurosity_sdk
from dotenv import load_dotenv
import os
import time

load_dotenv()

neurosity = neurosity_sdk({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

info = neurosity.get_info()
print(info)


def callback(data):
    print(data)


neurosity.focus(callback)

try:
    # include code to run the program
    time.sleep(10)
    print("Exiting after 10 seconds - cleaning up")
    neurosity.exit_handler()
    print("Cleaned up")
except (KeyboardInterrupt, SystemExit):
    # handle the keyboard interrupt or program halt
    print("Keyboard interrupt or program halt - cleaning up")
    neurosity.exit_handler()
    print("Cleaned up")
