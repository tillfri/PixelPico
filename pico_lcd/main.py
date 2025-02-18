import gc
import random
import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
from urllib import urequest
import ujson
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import pngdec
from pimoroni import Button
import time

# Define buttons
#button_a = Button(12)
#button_b = Button(13)
button_x = Button(14)
#button_y = Button(15)

# Set up graphics
graphics = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
graphics.set_backlight(0.7)

BASE_URL = "http://192.168.178.21:8000"
SCENE_LIST_ENDPOINT = f"{BASE_URL}/scenes"


def status_handler(mode, status, ip):
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"

# Connect to Wi-Fi
network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))


# Fetch list of scenes
response = urequest.urlopen(SCENE_LIST_ENDPOINT)
response_data = response.read()
scenes = ujson.loads(response_data)['scenes']
del response_data
response.close()
selected_scene = random.choice(scenes)
gc.collect()

# Fetch number of images in the selected scene
COUNT_ENDPOINT = f"{BASE_URL}/count/{selected_scene}"
response = urequest.urlopen(COUNT_ENDPOINT)
response_data = response.read()
NUMBER_OF_IMAGES = ujson.loads(response_data)['count']
del response_data
response.close()
gc.collect()

# Reserve 40kB for png images, if the image is larger the image will not be displayed
LEN_DATA = 1024 * 40
data = bytearray(LEN_DATA)
png = pngdec.PNG(graphics)
print(gc.mem_free())
gc.collect()

while(True):
    # Loop through image numbers for the selected scene
    for frame_number in range(NUMBER_OF_IMAGES):
        url = f"{BASE_URL}/image/{selected_scene}/{frame_number:04d}"
        #print(f"Requesting URL: {url}")
        print(gc.mem_free())
        for i in range(LEN_DATA):
            data[i] = 0  # Zero out old data
        
        # Open the URL and read image data
        socket = urequest.urlopen(url)
        del url

        socket.readinto(data)
        socket.close()
        print(gc.mem_free())
        gc.collect()
        
        # Now we use pngdec to decode the PNG image
        png.open_RAM(data)
        png.decode(0, 0, scale=1)  # Adjust scale if needed
        graphics.update()
        print(gc.mem_free())
        #print(f"Displayed image {frame_number:04d}")
        gc.collect()
        if button_x.read():
            time.sleep(1)
            break
        # Optional: Wait a bit before loading the next image
        #time.sleep(1)
    print("Selecting new scene...")
    selected_scene = random.choice(scenes)
    COUNT_ENDPOINT = f"{BASE_URL}/count/{selected_scene}"
    response = urequest.urlopen(COUNT_ENDPOINT)
    response_data = response.read()  # Read the response
    NUMBER_OF_IMAGES = ujson.loads(response_data)['count']
    del response_data
    response.close()
    gc.collect()
