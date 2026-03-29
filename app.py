"""
Streamlit web app for the Image Collage Generator.
Allows users to upload a target image and source images, tune parameters,
and generate a photomosaic collage in the browser.
"""

import io
import hashlib
import os
import tempfile
import time
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

from src.categorize_images import SourceImagePalette, categorize_single_image

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Image Collage Generator",
    page_icon="🎨",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
for key, default in [
    ("palette", None),
    ("palette_key", None),      # hash of source files to detect changes
    ("palette_tmpdir", None),   # temp dir holding source files for rendering
    ("collage", None),
    ("target_image", None),
    ("processing_time", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _files_hash(uploaded_files) -> str:
    """Compute a deterministic hash over a list of UploadedFile objects."""
    h = hashlib.md5()
    for f in sorted(uploaded_files, key=lambda x: x.name):
        h.update(f.name.encode())
        h.update(str(f.size).encode())
    return h.hexdigest()


def build_palette(uploaded_files, status_placeholder):
    """
    Save uploaded files to a temp directory and build a SourceImagePalette.

    The temp directory is kept alive so render_collage can open the files
    later via SourceImage.filepath.  The caller is responsible for cleaning
    up the previous tmpdir before calling this function.

    Returns (SourceImagePalette, tmpdir_path).
    """
    import shutil

    palette = SourceImagePalette()
    tmpdir = tempfile.mkdtemp(prefix="collage_sources_")

    return palette, tmpdir


def render_collage(
    target: Image.Image,
    palette: SourceImagePalette,
    num_cols: int,
    num_rows: int,
    progress_bar,
) -> Image.Image:
    """
    Render the photomosaic.

    Divides *target* into a num_cols × num_rows grid, finds the closest
    source image for each tile by average RGB colour, and assembles the
    final mosaic.  Tile dimensions are computed from the image size so
    the output is the same resolution as the (cropped) target.
    """
    
    return mosaic


def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Encode a PIL Image to bytes for download."""
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def show_image_previews(uploaded_files, max_cols: int = 8):
    """Display thumbnail previews for a list of UploadedFile objects."""
    cols = st.columns(min(len(uploaded_files), max_cols))
    for i, f in enumerate(uploaded_files):
        with cols[i % max_cols]:
            img = Image.open(f)
            img.thumbnail((120, 120))
            st.image(img, caption=f.name, use_container_width=False)


# ---------------------------------------------------------------------------
# App layout
# ---------------------------------------------------------------------------

st.title("🎨 Image Collage Generator")
st.markdown(
    """
    Turn any photo into a **photomosaic** — a collage built entirely from your
    own source images, each chosen by colour similarity.

    **How to use:**
    1. Upload a **target image** (the photo you want to recreate).
    2. Upload **source images** (the "tiles" — more variety = better results).
    3. Adjust the grid and matching settings in the sidebar.
    4. Click **Generate Collage** and download your result.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar — parameters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    grid_cols = st.slider("Grid columns", min_value=10, max_value=100, value=40, step=1,
                          help="Number of tile columns across the output image.")
    grid_rows = st.slider("Grid rows",    min_value=10, max_value=100, value=30, step=1,
                          help="Number of tile rows down the output image.")

    with st.expander("Advanced settings"):
        match_method = st.selectbox(
            "Colour matching method",
            options=["Euclidean (faster)", "Delta E (perceptual)"],
            index=0,
            help=(
                "**Euclidean** computes distance in RGB space — fast and usually good.\n\n"
                "**Delta E** uses perceptual CIE LAB space — slower but more accurate."
            ),
        )

    st.divider()
    st.markdown("**Minimum recommended sources:** 20+  \nMore unique colours → better collage.")

# ---------------------------------------------------------------------------
# Main columns — uploaders
# ---------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🖼️ Target image")
    target_file = st.file_uploader(
        "Upload the photo to recreate",
        type=["jpg", "jpeg", "png", "webp"],
        key="target_uploader",
    )

    if target_file:
        target_pil = Image.open(target_file).convert("RGB")
        st.session_state.target_image = target_pil
        st.image(target_pil, caption=f"{target_file.name}  ({target_pil.size[0]}×{target_pil.size[1]}px)", use_container_width=True)

with col_right:
    st.subheader("🗂️ Source images (tiles)")
    source_files = st.file_uploader(
        "Upload the images that will become tiles",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="source_uploader",
    )

    if source_files:
        st.caption(f"{len(source_files)} image(s) uploaded")
        show_image_previews(source_files, max_cols=8)

st.divider()

# ---------------------------------------------------------------------------
# Validation & Generate button
# ---------------------------------------------------------------------------
ready = bool(target_file and source_files)

if not target_file:
    st.info("ℹ️ Upload a target image to get started.")
elif not source_files:
    st.info("ℹ️ Upload at least one source image.")
elif len(source_files) < 5:
    st.warning("⚠️ Fewer than 5 source images will produce a low-quality collage. Upload more for better results.")

generate_clicked = st.button(
    "✨ Generate Collage",
    type="primary",
    disabled=not ready,
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# Generation pipeline
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------
