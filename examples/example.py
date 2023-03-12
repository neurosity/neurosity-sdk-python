from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import signal

load_dotenv()

# def signal_handler(sig, frame):
#     # set a flag or perform some other action to gracefully exit the program
#     exit(0)

# signal.signal(signal.SIGINT, signal_handler)

neurosity = NeurositySDK({
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
    pass
except (SystemExit):
    pass
