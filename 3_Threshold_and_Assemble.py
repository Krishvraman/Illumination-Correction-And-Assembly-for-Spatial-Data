import os
import pyvips
import sys
import tifffile
import argparse

scale=1
def parse_tile_info(filename):
    """
    Extracts x, y, width, and height from the filename.
    """
    parts = filename.split("_")
    x = int(parts[-4].split("-")[1])
    y = int(parts[-3].split("-")[1])
    w = int(parts[-2].split("-")[1])
    h = int(parts[-1].split("-")[1].split(".")[0])
    return x, y, w, h


def save_image(im, output_path):
    im = im.copy()
    im.set_type(pyvips.GValue.gint_type, "page-height", im.height)
    im.set_type(pyvips.GValue.gstr_type, "image-description",
                f"""<?xml version="1.0" encoding="UTF-8"?>
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
        <Image ID="Image:0">
            <!-- Minimum required fields about image dimensions -->
            <Pixels DimensionOrder="XYCZT"
                    ID="Pixels:0"
                    SizeC="{im.bands}"
                    SizeT="1"
                    SizeX="{im.width}"
                    SizeY="{im.height}"
                    SizeZ="1"
                    Type="uint8">
            </Pixels>
        </Image>
    </OME>""")

    im.tiffsave(output_path, compression="lzw", tile=True,
                pyramid=True, subifd=True)



def get_full_image_dimensions(input_folder):
    """
    Calculate the dimensions of the full image by determining the max extents
    from all tiles.
    """
    max_x, max_y, w, h = 0, 0, 0, 0
    for file in os.listdir(input_folder):
        if file.endswith("tif"):
            x, y, tile_w, tile_h = parse_tile_info(file)
            max_x = max(max_x, x + tile_w)
            max_y = max(max_y, y + tile_h)
            w, h = tile_w, tile_h
    return max_x, max_y

def assemble_tiles(input_folder, output_file):
    """
    Assemble the tiles into a single large image.
    """
    # Determine full image size
    full_width, full_height = get_full_image_dimensions(input_folder)
    full_image = pyvips.Image.black(full_width/scale, full_height/scale)

    count=0
    # Insert each tile into the full image
    for file in os.listdir(input_folder):
        if file.endswith(".tif"):
            x, y, _, _ = parse_tile_info(file)
            tile_path = os.path.join(input_folder, file)
            tile = pyvips.Image.new_from_file(tile_path)
            full_image = full_image.insert(tile, x/scale, y/scale)
            print(count)
            count+=1

    print("Insertion done")

    save_image(full_image, output_file)
    
   
def perform_thresholding(input_folder, intermediate_folder,threshold_value):
    count=0
    # Insert each tile into the full image
    for file in os.listdir(input_folder):
        if file.endswith(".tif"):
            x, y, _, _ = parse_tile_info(file)
            tile_path = os.path.join(input_folder, file)
            tile = tifffile.imread(tile_path)
            thresholded = tile.copy()
            thresholded[tile < threshold_value] = 0

			# Output_ tile save path
            thresholded_tile_path = os.path.join(intermediate_folder, file)
            tifffile.imwrite(thresholded_tile_path, thresholded)
            print(count)
            count+=1

    print("Thresholding done")
    

if __name__ == "__main__":
    # Define input folder and output file
    parser = argparse.ArgumentParser(description="Tile correction and assembly")
    parser.add_argument("dir_name", type=str, help="Directory name to process")
    parser.add_argument("threshold", type=float, help="Threshold value to use")
    args = parser.parse_args()

    dir_name = args.dir_name
    threshold = args.threshold

    main_folder = os.path.join('',dir_name) # For any additiona parent paths pass it inside the ''

    input_folder = os.path.join(main_folder,'FIJI_Output')
    intermediate_folder = os.path.join('',dir_name+'_THRESH')# For any additiona parent paths pass it inside the ''
    output_file = os.path.join('', dir_name+'.tif')# For any additiona parent paths pass it inside the ''

    os.makedirs(intermediate_folder)
    print(f"Created thresholded tile folder: {intermediate_folder}")
    
    # Perform threshold
    perform_thresholding(input_folder, intermediate_folder,threshold)
    
   
    # Assemble the tiles
    assemble_tiles(intermediate_folder, output_file)
    print("Assembly complete! Full image saved at:", output_file)
