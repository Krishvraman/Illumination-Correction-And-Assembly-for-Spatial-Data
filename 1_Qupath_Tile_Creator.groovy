extension = '.tif'

// Get the current image (supports 'Run for project')
def imageData = getCurrentImageData()

// Define output path (here, relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())

Tile_save_path = args[0] // Replace with path or pass argument

def pathOutput = buildFilePath(Tile_save_path)
mkdirs(pathOutput)

// To export at full resolution
double downsample = 1

// Define the channel name to filter
//def channelNameFilter = "CD66b" // Replace this with your desired channel name

def channelNameFilter = args[1]


println('Saving Tiles for Channel: ' + channelNameFilter)

// Create an exporter that requests corresponding tiles from the original & labeled image servers
new TileExporter(imageData)
    .downsample(downsample)      // Define export resolution
    .imageExtension(extension)   // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
    .tileSize(960,720)               // Define size of each tile, in pixels  - Change tiling depending on imaging modality paramter
    .annotatedTilesOnly(false)   // If true, only export tiles if there is a (classified or unclassified) annotation present
    .overlap(0)                  // Define overlap, in pixel units at the export resolution
    .channels(channelNameFilter) // Select channel
    .writeTiles(pathOutput)      // Write tiles to the specified directory

println('Tiles for Channel: ' + channelNameFilter + ' Saved')

def dirOutput = new File(pathOutput)


for (def file in dirOutput.listFiles()) {
    // Skip if not a file, hidden, or wrong extension
    if (!file.isFile() || file.isHidden() || !file.getName().endsWith(extension))
        continue
        
    def fileName = file.getName()
    
    // First apply all replacements
    def newName = fileName.replaceAll("=", "-")
                         .replaceAll("\\[", "_")
                         .replaceAll("\\]", "")
                         .replaceAll(",", "_")
                         .replaceAll(" ", "")
    
    // Then extract portion after '#' if it exists
    if (newName.contains('#')) {
        newName = newName.split('#')[1]
        
        // Skip if no change needed
        if (fileName == newName)
            continue
            
        def fileUpdated = new File(file.getParent(), newName)
        //println("Renaming ${file.getName()} ---> ${fileUpdated.getName()}")
        file.renameTo(fileUpdated)
    }
}



println('Tiles Generated')
