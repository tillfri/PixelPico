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


def status_handler(mode, status, ip):
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"

# Connect to Wi-Fi
network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
#uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
def print_message(message):
    print(message)
    graphics.set_font("bitmap8")
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    graphics.text(message, 7, 25, wordwrap=240, scale=2)
    graphics.update()
    time.sleep(3)

try:
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
except Exception as e:
    error_message = "Error: {}".format(e)
    print_message(error_message)
    raise e


def fetch_json(url):
    """Fetch JSON data from the given URL, retrying on failure."""
    while True:
        try:
            response = urequest.urlopen(url)
            response_data = response.read()
            data = ujson.loads(response_data)
            del response_data
            response.close()
            gc.collect()
            return data
        except OSError as e:
            print(f"Error fetching {url}: {e}")
            print("Sleeping for 30 seconds before retrying...")
            error_message = "Error: {}".format(e)
            print_message(error_message)
            time.sleep(30)

def display_scenes():
    BASE_URL = "http://192.168.178.21:8000"
    SCENE_LIST_ENDPOINT = f"{BASE_URL}/scenes"
    # Fetch list of scenes
    scenes = fetch_json(SCENE_LIST_ENDPOINT).get('scenes', [])
    if not scenes:
        print("No scenes available.")
        return
    else:
        selected_scene = random.choice(scenes)

        # Fetch number of images in the selected scene
        COUNT_ENDPOINT = f"{BASE_URL}/count/{selected_scene}"
        NUMBER_OF_IMAGES = fetch_json(COUNT_ENDPOINT).get('count', 0)
        
        print(f"Selected scene: {selected_scene}, Number of images: {NUMBER_OF_IMAGES}")

    gc.collect()
    # Reserve 38kB for png images, if the image is larger the image will not be displayed
    LEN_DATA = 1024 * 38
    data = bytearray(LEN_DATA)
    png = pngdec.PNG(graphics)
    print(gc.mem_free())
    gc.collect()
    while(True):
        try:
            # Loop through image numbers for the selected scene
            for frame_number in range(NUMBER_OF_IMAGES):
                url = f"{BASE_URL}/image/{selected_scene}/{frame_number:04d}"
                #print(f"Requesting URL: {url}") 
                for i in range(LEN_DATA): data[i] = 0
                
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
                #print(f"Displayed image {frame_number:04d}")
                print(gc.mem_free())

                gc.collect()
                if button_x.read():
                    time.sleep(1)
                    break
                # Optional: Wait a bit before loading the next image
                #time.sleep(1)
            print("Selecting new scene...")
            if button_x.read():
                print("exiting display scene")
                time.sleep(1)
                return
            selected_scene = random.choice(scenes)
            COUNT_ENDPOINT = f"{BASE_URL}/count/{selected_scene}"
            NUMBER_OF_IMAGES = fetch_json(COUNT_ENDPOINT).get('count', 0)
            
        except Exception as e:
            # Handle the exception by printing the error to the display
            error_message = "Error Type: {}\nMessage: {}\n UNRECOVERABLE".format(type(e).__name__, str(e))
            print_message(error_message)
            time.sleep(30)

def other_mode():
    while(True):
        print("We are in a new mode")
        if button_x.read():
                print("exiting other mode")
                time.sleep(1)
                break
        time.sleep(10)


while(True):
    try:
        display_scenes()
        gc.collect()
        other_mode()
        gc.collect()
    except Exception as e:
            # Handle the exception by printing the error to the display
            error_message = "Error Type: {}\nMessage: {}\n UNRECOVERABLE".format(type(e).__name__, str(e))
            print_message(error_message)
            time.sleep(30)
    

