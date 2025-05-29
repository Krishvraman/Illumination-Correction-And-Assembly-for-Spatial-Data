# Tile-Based Illumination Correction and Assembly Pipeline

This repository contains a set of scripts for preprocessing large microscopy images by correcting for uneven illumination, removing background noise, and reassembling processed tiles into a standardized final image for downstream analysis.

## Key Idea

To correct for uneven illumination and prepare the data for analysis, the following preprocessing pipeline is performed:

1. **Tile Generation**: Raw microscopy data is split into full-resolution tiles by channel using a QuPath Groovy script.
2. **Background Subtraction**: A rolling ball algorithm is applied on downsampled tile images to create a background mask, which is then subtracted from the original tiles.
3. **Upsampling and Thresholding**: Background-subtracted images are upsampled and a global intensity threshold is applied to eliminate low-intensity background noise.
4. **Tile Reassembly**: All processed tiles are merged back into a single full-resolution TIFF image, retaining spatial coherence.

## 📁 Directory Structure

```
repo/
├── generate_tiles.groovy     # QuPath Groovy script to export tiles
├── fiji_macro.ijm            # ImageJ macro for background subtraction
├── threshold_and_assemble.py # Python script for thresholding and reassembly
├── assemble_only.py          # Alternative: Assemble tiles without thresholding
├── README.md
```

---

## Requirements

- **QuPath** (for tile export)
- **Fiji / ImageJ** with Rolling Ball plugin
- **Python 3.8+**
  - `pyvips`
  - `tifffile`
  - `argparse`
  - `numpy`

Install dependencies using pip:

```bash
pip install pyvips tifffile numpy
```

---

##  Usage

### 1. Generate Tiles from Raw Images

Run the `generate_tiles.groovy` script within QuPath:

```groovy
// Args:
//   [0] = output tile folder path
//   [1] = desired channel name
```

Make sure the image is loaded and selected in QuPath, then run:

```groovy
Tile_save_path = "/path/to/output_tiles"
channelNameFilter = "YourChannelName"
```

---

### 2. Background Subtraction using Fiji

Use `fiji_macro.ijm` for background subtraction:

- Drag the tile folder into Fiji.
- Run the macro with the rolling ball
- Processed tiles will be saved to a new output folder.

---

### 3. Threshold and Assemble Tiles

Use the Python script to apply thresholding and reassemble tiles into a single image:

```bash
python threshold_and_assemble.py <tile_folder_name> <threshold_value>
```

Example:

```bash
python threshold_and_assemble.py Experiment1 2
```

This will:
- Threshold all `.tif` tiles using the value `2`
- Save thresholded tiles in a new folder
- Reassemble them into a final `.tif` image

---

### 4. Assemble Only (Optional)

If thresholding is not needed, use the `assemble_only.py` script:

```bash
python assemble_only.py /path/to/tiles /path/to/output/final_image.tif
```

---

##  Example Workflow

```bash
# Step 1: Export tiles from QuPath
# Step 2: Background subtract in Fiji using provided .ijm macro
# Step 3: Run
python threshold_and_assemble.py MyExperiment 12
```

---

## Notes

- Ensure filenames follow the required `x-<X>_y-<Y>_w-<W>_h-<H>.tif` format for parsing coordinates.
- The pipeline is optimized for large histology or microscopy images where uneven illumination skews analysis.
