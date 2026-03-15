from PIL import Image
import numpy as np
from categorize_images import SourceImage, SourceImagePalette, categorize_all_images



def render_collage(target_image: Image.Image,
                   palette: SourceImagePalette,
                   tile_size: int = 40,
                   method: str = "euclidean") -> Image.Image:

    # Crop to clean tile grid

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Extract tile and compute average color

            # Use your existing matching function

            # Load image from filepath

            # Resize to tile

    return mosaic

# Render collage for all images in the dataset
