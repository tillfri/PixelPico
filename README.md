# Raspberry Pi Pico WH - Pimoroni Display Pack 2.0 Image Sequence Viewer

## Overview
This project uses a Raspberry Pi Pico WH with a Pimoroni Display Pack 2.0 to display looping image sequences. The images are served from a FastAPI backend running in a Docker container. The Pico fetches images over WiFi and randomly selects a scene to display. Pressing and holding the X button will trigger a new random scene selection.

## Requirements
### Hardware
- **Raspberry Pi Pico WH** (WiFi-enabled)
- **Pimoroni Display Pack 2.0**

### Software & Tools
- **MicroPython** (Pimoroni firmware for the Display Pack)
- **Docker** (for running the FastAPI server)
- **FastAPI** (to serve image sequences)

## Getting Started

### FastAPI Server Setup
1. Build the Docker image using the provided `Dockerfile`:
   ```sh
   docker build -t fastapi-scenes .
   ```
2. Create a `scenes` directory and add subdirectories named after different scenes.
3. Place PNG images inside these scene directories.
   - Images must be in `.png` format.
   - Each image should not exceed **40kB** in size.
4. Run the FastAPI container:
   ```sh
   docker run -d -p 8000:8000 -v $(pwd)/scenes:/app/scenes fastapi-scenes
   ```
5. Note the IP address of the machine running the container, as you will need it for the Pico setup.

### Raspberry Pi Pico Setup
⚠️ **Backup your Pico before proceeding!** Critical failures may require a full flash reset.

1. **Install Pimoroni MicroPython Firmware** on your Pico. You can download it from the [Pimoroni website](https://github.com/pimoroni/pimoroni-pico/releases).
2. **Copy the contents of `pico_lcd/` onto your Pico.**
3. **Configure WiFi:** Edit `WIFI_CONFIG` in the code to match your network settings.
4. **Set FastAPI Server URL:** Adjust `BASE_URL` to point to the IP and port of the FastAPI container.

## Features
- The Pico randomly selects a scene from your `scenes` directory.
- It displays all images inside the selected scene sequentially.
- Once finished, it randomly selects a new scene (which can be the same as the previous one).
- Holding the **X Button** forces an early random scene selection.
- Designed for smooth animations (no extra delay between frames).
- **Optional Picture Frame Mode:** Uncomment the `time.sleep()` line at the end of the scene loop to introduce a delay between frames, making it function more like a digital picture frame.

## License
This project is open-source under the MIT License.

