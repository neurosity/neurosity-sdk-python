from neurosity import neurosity_sdk
from dotenv import load_dotenv
import os
import time

load_dotenv()

sdk = neurosity_sdk({
    "device_id": "e903a615c23f7943e9d2869d4a9f1f3b",
    # "environment": "staging"
})

sdk.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

info = sdk.get_info()
print(info)

def callback(data):
    print(data)

unsubscribe = sdk.focus(callback)

time.sleep(3)
unsubscribe()
time.sleep(3)