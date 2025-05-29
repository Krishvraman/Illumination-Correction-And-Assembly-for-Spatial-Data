args = getArgument();
args_list=split(args,"=");

// Path parameters
input_folder=args_list[0] // Add path or pass argument from commandline 
output_folder=args_list[1]


run("Close All");

rolling_ball_size=18

File.openSequence(input_folder);
run("Scale...", "x=0.25 y=0.25 z=1.0 interpolation=Bicubic average process create");
rename("original");


run("Duplicate...", "duplicate");
rename("background");

// Create background
run("Subtract Background...", "rolling=18 create sliding disable stack");

// subtract background
imageCalculator("Subtract create stack", "original","background");


//Upscale
run("Scale...", "x=4 y=4 z=1.0 interpolation=Bicubic average process create");

setOption("ScaleConversions", false);
run("8-bit");


// save path
run("Image Sequence... ", "select="+output_folder+" dir="+output_folder+" format=TIFF use");

run("Quit");

