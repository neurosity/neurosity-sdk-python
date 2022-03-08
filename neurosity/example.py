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


unsubscribe = neurosity.focus(callback)

time.sleep(10)
unsubscribe()
