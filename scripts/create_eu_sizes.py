import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc
import Rhino
import os
import time

# Function to calculate scale factor based on circumference
def scale_factor_from_circumference(original_circ, target_circ):
    return target_circ / original_circ

# Read the arguments from the temporary file
temp_file_path = os.path.join(os.getenv('TEMP'), 'RingSize.txt')
with open(temp_file_path, 'r') as file:
    args = file.readlines()
    current_circumference = float(args[0].strip())  # Convert to float
    save_path = os.path.dirname(args[1].strip()) 
    sizes_directory = os.path.join(save_path, "sizes")

# Check if the sizes directory exists, and create it if it doesn't
if not os.path.exists(sizes_directory):
    os.makedirs(sizes_directory)

layers_to_hide = []
for prefix in ["Gem", "CADRAWS", "Cutting", "Rend", "rend", "REND"]:
    layers_to_hide.extend(functions.toggle_layers_with_prefix(prefix))

# Range of target circumferences
target_circumferences = range(45, 75)  # 45 to 70 inclusive

# Get the ID of the selected ring object
selected_objects = rs.SelectObjects(rs.AllObjects())
if not selected_objects:
    print("No objects selected. Please select one ring object.")
    exit()

# Iterate over the target circumferences
for target_circ in target_circumferences:
    rs.SelectObjects(rs.AllObjects())
    # Calculate the scale factor
    scale_factor = scale_factor_from_circumference(current_circumference, target_circ)
    current_circumference = target_circ
    
    rs.Command("_-Scale " + "_Enter " + str(scale_factor) + " _Enter", False)
    # Export the scaled ring to a file
    filename = "ring_size{0}.stl".format(target_circ)
    full_path = os.path.join(sizes_directory, filename)

    rs.Command('-_Export "{}" _Enter _Enter'.format(full_path))
    
print("Export completed.")
os.remove(temp_file_path)


sc.doc.Modified = False
#rs.Command("_Exit")