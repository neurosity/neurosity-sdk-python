# You need to install the python dashing if you want to run this code
try:
    from dashing import HSplit, VSplit, HGauge, VGauge, HBrailleChart
except ImportError:
    print("The dashing module is not installed. Please install it using:")
    print("pip install dashing")
    exit(1)  # Exit the script if dashing is not installed

import os
from dotenv import load_dotenv
from neurosity import NeurositySDK
from time import sleep

# Load environment variables
load_dotenv()

# Initialize Neurosity SDK with the device ID from environment variables
neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

# UI field paths for displaying brainwave band powers
FIELD_PATHS = {
    "alpha": (0, 1, 0),
    "beta": (0, 1, 1),
    "delta": (0, 1, 2),
    "gamma": (0, 1, 3),
    "theta": (0, 1, 4)
}

def neurosity_login():
    """Attempt to log into Neurosity."""
    try:
        neurosity.login({
            "email": os.getenv("NEUROSITY_EMAIL"),
            "password": os.getenv("NEUROSITY_PASSWORD")
        })
        print("Logged in successfully.")
        return True
    except Exception as e:
        print(f"Failed to log in: {e}")
        return False

def callback_focus(data):
    """Handle focus data callback."""
    ui.items[0].items[0].items[0].value = int(data["probability"] * 100)

def callback_calm(data):
    """Handle calm data callback."""
    ui.items[0].items[0].items[1].value = int(data["probability"] * 100)

def callback_brainwaves_power_by_band(data):
    """Handle brainwaves power by band data callback."""
    for band, values in data['data'].items():
        average_power = round(sum(values) / len(values))
        path = FIELD_PATHS[band]
        ui.items[path[0]].items[path[1]].items[path[2]].value = average_power

def callback_brainwaves_raw(data):
    """Handle raw brainwaves data callback."""
    for channel_index, channel in enumerate(data['data']):
        ui.items[1].items[channel_index].append(round(sum(channel) / len(channel)))

def setup_ui():
    """Set up the user interface."""
    global ui
    ui = HSplit(
        VSplit(
            HSplit(
                VGauge(val=0, title="Focus", border_color=2, color=4),
                VGauge(val=5, title="Calm", border_color=2, color=3),
            ),
            HSplit(
                VGauge(val=0, title="Alpha", border_color=2, color=1),
                VGauge(val=0, title="Beta", border_color=2, color=2),
                VGauge(val=0, title="Delta", border_color=2, color=3),
                VGauge(val=0, title="Gamma", border_color=2, color=4),
                VGauge(val=0, title="Theta", border_color=2, color=5),
            )  
        ),
        VSplit(
            HBrailleChart(border_color=2, color=1, title="CP6"),
            HBrailleChart(border_color=2, color=2, title="F6"),
            HBrailleChart(border_color=2, color=3, title="C4"),
            HBrailleChart(border_color=2, color=4, title="CP4"),
            HBrailleChart(border_color=2, color=5, title="CP3"),
            HBrailleChart(border_color=2, color=6, title="F5"),
            HBrailleChart(border_color=2, color=7, title="C3"),
            HBrailleChart(border_color=2, color=7, title="CP5"),
        ),
    )

if __name__ == '__main__':
    
    if neurosity_login():
        setup_ui()
        neurosity.calm(callback_calm)
        neurosity.focus(callback_focus)
        neurosity.brainwaves_power_by_band(callback_brainwaves_power_by_band)
        neurosity.brainwaves_raw(callback_brainwaves_raw)
        
        try:
            while True:
                sleep(1/25)  # Maintain a loop to keep the script running
                ui.display()
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down.")
        finally:
            print("Cleaning up resources.")
    else:
        print("Failed to initialize Neurosity device.")
