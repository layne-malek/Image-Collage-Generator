import os
import yaml
from PIL import Image
from typing import Dict, Any
import time

# Import our project modules
from src.categorize_images import (
    categorize_all_images, 
    load_palette, 
    save_palette,
    SourceImagePalette
)
from src.segment_target import segment_image, visualize_segments
from src.render_collage import render_collage


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config.yaml file
        
    Returns:
        Dictionary containing configuration parameters
    """
    
    return config


def ensure_directories_exist(config: Dict[str, Any]) -> None:
    """
    Create necessary directories if they don't exist.
    
    Args:
        config: Configuration dictionary
    """
    directories = [
        config['source_images']['directory'],
        config['target_images']['directory'],
        config['collage']['output_directory'],
        os.path.dirname(config['source_images']['cache_file'])
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def load_or_build_palette(config: Dict[str, Any]) -> SourceImagePalette:
    """
    Load source image palette from cache or build it from scratch.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        SourceImagePalette containing all source images
    """
    cache_file = config['source_images']['cache_file']
    source_dir = config['source_images']['directory']
    supported_formats = config['source_images']['supported_formats']
    
    # Check if cache exists
    if os.path.exists(cache_file):
        print(f"✓ Found cached source images at: {cache_file}")
        try:
            palette = load_palette(cache_file)
            return palette
        except Exception as e:
            print(f"✗ Failed to load cache: {e}")
            print("  Building palette from scratch...")
    
    # Build palette from source images
    print(f"\nScanning source images directory: {source_dir}")
    palette = categorize_all_images(source_dir, supported_formats)
    
    if len(palette) == 0:
        raise ValueError(
            f"No source images found in {source_dir}!\n"
            f"Please add images to this directory."
        )
    
    # Save to cache for future use
    print(f"\nCaching palette for future use...")
    save_palette(palette, cache_file)
    
    return palette


def get_target_image_path(config: Dict[str, Any]) -> str:
    """
    Get the target image path from user or use first image in directory.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Path to target image
    """
    
    # List available target images

    # If only one image, use it automatically
    
    # Multiple images - let user choose


def create_collage(target_image_path: str, palette: SourceImagePalette, 
                   config: Dict[str, Any]) -> Image.Image:
    """
    Create the final collage by matching target segments to source images.
    
    Args:
        target_image_path: Path to target image
        palette: SourceImagePalette with all source images
        config: Configuration dictionary
        
    Returns:
        PIL Image of the final collage
    """
    # Load target image
    
    # Get grid dimensions from config
    
    
    # Optional: Save segment visualization for debugging

    
    # Calculate tile size (use base segment size from metadata)
    
    
    # Render the collage
    
    return collage


def save_collage(collage: Image.Image, target_image_path: str, 
                 config: Dict[str, Any]) -> str:
    """
    Save the final collage with a descriptive filename.
    
    Args:
        collage: PIL Image of the collage
        target_image_path: Original target image path
        config: Configuration dictionary
        
    Returns:
        Path to saved collage
    """
    # Create output filename
    
    # Save the collage


def print_banner():
    """Print a nice banner for the program."""
    print("\n" + "="*70)
    print(" "*20 + "IMAGE COLLAGE GENERATOR")
    print("="*70)


def print_summary(config: Dict[str, Any], palette_size: int, 
                  output_path: str, elapsed_time: float):
    """
    Print summary statistics after completion.
    
    Args:
        config: Configuration dictionary
        palette_size: Number of source images
        output_path: Path to saved collage
        elapsed_time: Time taken to create collage
    """
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Source images used: {palette_size}")
    print(f"Grid size: {config['collage']['grid_segments_x']}x{config['collage']['grid_segments_y']}")
    print(f"Total segments: {config['collage']['grid_segments_x'] * config['collage']['grid_segments_y']}")
    print(f"Output saved to: {output_path}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print("="*70 + "\n")


def main():
    """
    Main driver function that orchestrates the entire collage creation process.
    """
    start_time = time.time()
    
    try:
        # Step 1: Print banner
        
        # Step 2: Load configuration
        
        # Step 3: Ensure directories exist
        
        
        # Step 4: Load or build source image palette
       
        
        # Step 5: Get target image
        
        
        # Step 6: Create the collage
        
        
        # Step 7: Save the result
        
        
        # Calculate elapsed time
        
        
        # Print summary
        
        # Success!
        print("✓ SUCCESS! Your collage is ready.\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user.")
        return 1
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
