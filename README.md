# Neurosity Python SDK

Welcome to the official Neurosity Python SDK. This library is compatible with Python 3.

## Table of Contents

- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Methods](#streaming-data)
  - [sdk.login()](#login)
  - [sdk.brainwaves_raw()](#brainwaves_raw)
  - [sdk.brainwaves_raw_unfiltered()](#brainwaves_raw_unfiltered)
  - [sdk.brainwaves_psd()](#brainwaves_psd)
  - [sdk.brainwaves_power_by_band()](#brainwaves_power_by_band)
  - [sdk.add_marker()](#add_marker)
  - [sdk.signal_quality()](#signal_quality)
  - [sdk.accelerometer()](#accelerometer)
  - [sdk.calm()](#calm)
  - [sdk.focus()](#focus)
  - [sdk.kinesis(label)](#kinesis)
  - [sdk.get_info()](#get_info)
  - [sdk.status_once()](#get_status)
  - [sdk.settings_once()](#get_settings)
  - [sdk.status()](#stream_status)
  - [sdk.settings()](#stream_settings)

## Getting Started

To get started with the Neurosity SDK, you'll need:

- Your device ID
- Your Neurosity account email
- Your Neurosity account password

To get your 32-character Neurosity device ID, use the Neurosity mobile app available for iOS and Android. Go to `Settings -> Device Info`.

> 💡 Never hardcode your email and password directly in your Python code. Instead, create a `.env` file in the root of your project and add:

```bash
NEUROSITY_EMAIL=your email here
NEUROSITY_PASSWORD=your password here

```

## Authentication

### Authentication Code Example

```python
from neurosity import neurosity_sdk
from dotenv import load_dotenv
import os

load_dotenv()

sdk = neurosity_sdk({
    "device_id": "e903a615c23f7943e9d2869d4a9f1f3b",
})

sdk.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})
```

## Streaming Data

### Raw Data

```python
def callback(data):
    print("data", data)

unsubscribe = sdk.brainwaves_raw(callback)
time.sleep(4)
unsubscribe()
```

### Adding Markers

```python
def callback(data):
    print("data", data)

unsubscribe = sdk.brainwaves_raw(callback)
time.sleep(2)
sdk.add_marker("eyes-closed")
time.sleep(2)
unsubscribe()
```

## MIT
