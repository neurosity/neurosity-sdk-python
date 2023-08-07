from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import time

load_dotenv()

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

unsubscribe = neurosity.brainwaves_raw(callback)
time.sleep(5)
unsubscribe()
print("Done with example.py")
