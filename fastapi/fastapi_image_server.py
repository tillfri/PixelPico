import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Directory containing the scenes
scenes_directory = "scenes"


# Endpoint to list all scenes
@app.get("/scenes")
async def list_scenes():
    # List all directories in the "scenes" directory
    scenes = [
        scene
        for scene in os.listdir(scenes_directory)
        if os.path.isdir(os.path.join(scenes_directory, scene))
    ]
    return {"scenes": scenes}


# Endpoint to serve the image for a specific scene and frame_number
@app.get("/image/{scene_name}/{frame_number}")
async def get_image(scene_name: str, frame_number: int):
    scene_directory = os.path.join(scenes_directory, scene_name)
    image_filename = f"frame_{frame_number:04d}.png"
    image_path = os.path.join(scene_directory, image_filename)

    if not os.path.isdir(scene_directory):
        return {"error": f"Scene {scene_name} not found"}
    if not os.path.exists(image_path):
        return {"error": f"Image frame {frame_number} not found in scene {scene_name}"}

    return FileResponse(image_path)


# Endpoint for retrieving the amount of images in the chosen scene
@app.get("/count/{scene_name}")
async def get_amount_images(scene_name: str):
    scene_directory = os.path.join(scenes_directory, scene_name)

    if not os.path.isdir(scene_directory):
        return {"error": f"Scene {scene_name} not found."}

    image_files = [f for f in os.listdir(scene_directory) if f.endswith(".png")]
    count = len(image_files)
    return {"count": count}
