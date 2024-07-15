import rhinoscriptsyntax as rs
import Rhino as rh
import Rhino.Render as rr
import Rhino.DocObjects as rd
import scriptcontext as sc
import os
import math

#########################################################################################
## HIDE OR SHOW LAYERS
def toggle_layers_with_prefix(prefix, action="hide"):
    """Toggle visibility of layers with a given prefix."""
    layers = [l for l in rs.LayerNames() if l.startswith(prefix)]
    
    if action == "hide":
        return [l for l in layers if rs.LayerVisible(l, False)]
    elif action == "show":
        [rs.LayerVisible(l, True) for l in layers]
        return []

###########################################################################################
## CREATE STL
def export_to_stl():
    """Export current Rhino doc to STL."""
    doc_path, doc_name = rs.DocumentPath(), rs.DocumentName()
    
    if not (doc_path and doc_name):
        print("Please save your Rhino file first.")
        return
    directory = os.path.dirname(doc_path)

    stl_filename = os.path.join(directory, os.path.splitext(doc_name)[0] + ".stl")

    layers_to_unhide = []
    for prefix in ["Gem", "CADRAWS", "Cutting", "Rend", "rend", "REND"]:
        layers_to_unhide.extend(toggle_layers_with_prefix(prefix))

    rs.SelectObjects(rs.AllObjects())
    rs.Command('-_Export "{}" _ExportFileAs=_Binary _Enter _Enter'.format(stl_filename))
    rs.UnselectAllObjects()

    for layer in layers_to_unhide:
        rs.LayerVisible(layer, True)
    
    rs.Command("_ZEA")
    if os.path.exists(stl_filename):
        os.startfile(stl_filename)

###########################################################################################
## CREATE STL FROM SELECTED OBJECTS
def export_selected_layer_as_stl(layer_name=None, i=None):
    """Export current Rhino doc to STL."""
    doc_path, doc_name = rs.DocumentPath(), rs.DocumentName()

    if not (doc_path and doc_name):
        print("Please save your Rhino file first.")
        return
    directory = os.path.dirname(doc_path)
    print(layer_name)
    any_selected_objects = select_objects_in_layer(layer_name)
    if any_selected_objects:
        rs.Command("_Isolate")
        parts = layer_name.split(str(i) + '_')
        stl_postfix = parts[1] if len(parts) > 1 else None
        if stl_postfix:
            stl_filename = os.path.join(directory, os.path.splitext(doc_name)[0] + '_' + stl_postfix + ".stl")
        else:
            stl_filename = os.path.join(directory, os.path.splitext(doc_name)[0] + '_' + str(i) + ".stl")

        layers_to_unhide = []
        for prefix in ["Gem", "CADRAWS", "Cutting", "Rend", "rend", "REND"]:
            layers_to_unhide.extend(toggle_layers_with_prefix(prefix))

        rs.SelectObjects(rs.AllObjects())
        rs.Command('-_Export "{}" _ExportFileAs=_Binary _Enter _Enter'.format(stl_filename))
        rs.Command("_Unisolate")
        rs.UnselectAllObjects()

        for layer in layers_to_unhide:
            rs.LayerVisible(layer, True)

        rs.Command("_ZEA")
        if os.path.exists(stl_filename):
            os.startfile(stl_filename)

###########################################################################################
## EXPORT STL BY NAME
def export_to_stl_by_file_name(file_name):
    """Export current Rhino doc to STL."""
    doc_path = rs.DocumentPath()
    rs.UnselectAllObjects()
    directory = os.path.dirname(doc_path)
    stl_filename = os.path.join(directory, file_name + ".stl")

    layers_to_unhide = []
    for prefix in ["Gem", "CADRAWS", "Cutting", "Rend", "rend", "REND"]:
        layers_to_unhide.extend(toggle_layers_with_prefix(prefix))

    rs.SelectObjects(rs.AllObjects())
    rs.Command('-_Export "{}" _ExportFileAs=_Binary _Enter _Enter'.format(stl_filename))
    rs.UnselectAllObjects()

    for layer in layers_to_unhide:
        rs.LayerVisible(layer, True)


##############################################################################################
## DELETE MATERIALS
def remove_all_materials():
    """Remove all materials from the document."""
    mats = [mat for mat in sc.doc.Materials]
    for mat in mats:
        sc.doc.Materials.Remove(mat)
    
    rms = [rm for rm in sc.doc.RenderMaterials]
    for rm in rms:
        sc.doc.RenderMaterials.Remove(rm)

##############################################################################################
## CREATE MATERIAL
def create_pbr_material(color, name, metallic=1.0, roughness=0.56, sheen=0.10, sheen_tint=0.90, opacity=1):
    """Create a PBR material and add it to the document."""
    pbr_material_type_guid = rr.ContentUuids.PhysicallyBasedMaterialType
    pbr_rm = rr.RenderContentType.NewContentFromTypeId(pbr_material_type_guid)
    sim = pbr_rm.SimulatedMaterial(rr.RenderTexture.TextureGeneration.Allow)
    pbr = sim.PhysicallyBased
    
    pbr.BaseColor = color
    pbr.Metallic = metallic
    pbr.Roughness = roughness
    pbr.Sheen = sheen
    pbr.SheenTint = sheen_tint
    pbr.Opacity = opacity
    
    new_pbr = rr.RenderMaterial.FromMaterial(pbr.Material, sc.doc)
    new_pbr.Name = name
    sc.doc.RenderMaterials.Add(new_pbr)

##############################################################################################
## SELECT OBJECTS THAT ARE IN LAYER NAMES
def select_objects_in_gem_layers_and_assign_material(material_name, layer_name="Gem"):
    """Select objects in given layers and assign a specified material."""
    gem_layers = [layer for layer in rs.LayerNames() if layer.startswith(layer_name)]
    for layer in gem_layers:
        objs = rs.ObjectsByLayer(layer)
        if objs:
            rs.SelectObjects(objs)
    if rs.SelectedObjects():
        rs.Command('_RenderAssignMaterialToObjects "{}"'.format(material_name), False)
    rs.UnselectAllObjects()

##############################################################################################
## SELECT OBJECTS THAT ARE NOT IN LAYER NAMES 
def select_objects_not_in_gem_layers_and_assign_material(material_name, layer_name="Gem"):
    """Select objects not in given layers and assign a specified material."""
    all_layers = rs.LayerNames()
    non_gem_layers = [layer for layer in all_layers if not layer.startswith(layer_name)]
    
    for layer in non_gem_layers:
        objs = rs.ObjectsByLayer(layer)
        if objs:
            rs.SelectObjects(objs)
    
    if rs.SelectedObjects():
        rs.Command('_RenderAssignMaterialToObjects "{}"'.format(material_name), False)
    rs.UnselectAllObjects()

##############################################################################################
## SELECTS OBJECTS IN GIVEN LAYER
def select_objects_in_layer(layer_name):
    all_layers = rs.LayerNames()
    any_objects = 0
    if layer_name in all_layers:
        objs = rs.ObjectsByLayer(layer_name)
        if objs:
            rs.SelectObjects(objs)
            any_objects = 1
    return any_objects

##############################################################################################
## SELECT ALL THE OBJECTS THAT START WITH NUMBER IN FRONT
def select_all_objects_starting_with_number(i):
    all_layers = rs.LayerNames()
    matching_layer_names = [item for item in all_layers if item.startswith(str(i) + '_')]
    for layer_name in matching_layer_names:
        select_objects_in_layer(layer_name)
    return matching_layer_names

##############################################################################################
## ASSIGN MATERIAL TO LAYER
def assign_material(material_name, layer_name):
    """Select objects not in given layers and assign a specified material."""
    all_layers = rs.LayerNames()
    
    if layer_name in all_layers:
        print(layer_name)
        objs = rs.ObjectsByLayer(layer_name)
        print(objs)
        if objs:
            rs.SelectObjects(objs)
    
    if rs.SelectedObjects():
        rs.Command('_RenderAssignMaterialToObjects "{}"'.format(material_name), False)
    rs.UnselectAllObjects()
    
###############################################################################################
## CREATE DIRECTORY
def create_directory(directory_name):
    """Creates a new directory within the current document's directory."""
    base_path = rs.DocumentPath()
    if not base_path:
        print("Please save the Rhino file first.")
        return None

    new_directory = os.path.join(os.path.dirname(base_path), directory_name)
    
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
        
    return new_directory

#################################################################################################
## CREATE IMAGE FOR VIEW
def capture_current_view(directory, view_name, width=1118, height=627):
    """Captures the current view and saves it to the specified directory."""
    capture_path = os.path.join(directory, "{}.png".format(view_name))
    rs.Command('-ViewCaptureToFile TransparentBackground=No W 1024 H 567 Scale 1 "{}" Enter'.format(capture_path), False)

    
##################################################################################################
## CREATE VIDEO FROM CAPTURES
def create_video_captures(directory_base):
    rs.Command("_-DocumentProperties _AnnotationStyles _ModelSpaceScaling=_Disabled _EnterEnd")
    align_all()

    all_objects = rs.AllObjects()
    visible_objects = [obj for obj in all_objects if not rs.IsObjectHidden(obj) and not rs.IsLayerLocked(rs.ObjectLayer(obj))]

    # Assume the entire model should be visible
    bounding_box = rs.BoundingBox(visible_objects)
    if not bounding_box: return

    center = rs.PointDivide(rs.PointAdd(bounding_box[0], bounding_box[6]), 2)

    # Determine the longest dimension of the bounding box to set the camera direction and distance
    dimensions = [rs.Distance(bounding_box[0], bounding_box[1]),
                  rs.Distance(bounding_box[0], bounding_box[3]),
                  rs.Distance(bounding_box[0], bounding_box[4])]
    longest_dimension = max(dimensions)

    # Assume dimensions calculated as before
    longest_dimension_index = dimensions.index(longest_dimension)

    # Initialize direction vector
    direction_vector = [0, 0, 0]

    # Set the corresponding direction based on the longest dimension
    if longest_dimension_index == 0:
        rs.Command("_SetView _World Front")
        rs.CurrentView("Front")
        rotate90()
        align_all()
        rs.Command("_SetView _World Left")
        rs.ViewDisplayMode("Left", "Rendered")
        rs.CurrentView("Left")

        viewPort = rs.CurrentView()
    elif longest_dimension_index == 1:
        # Longest dimension along Y-axis
        rs.Command("_SetView _World Front")
        rs.CurrentView("Front")
        rotate90()
        rs.Command("_SetView _World Right")
        rs.CurrentView("Right")
        rotate90()
        align_all()
        rs.Command("_SetView _World Left")
        rs.ViewDisplayMode("Left", "Rendered")
        rs.CurrentView("Left")
    elif longest_dimension_index == 2:
        # Longest dimension along Z-axis
        rs.Command("_SetView _World Front")
        rs.ViewDisplayMode("Front", "Rendered")
        rs.CurrentView("Front")

    viewPort = rs.CurrentView()
    rs.Command("_MaxViewport")
    rs.RotateView(viewPort, 1, 4)
    rh.RhinoApp.Wait()
    rs.Command("_ZEA")
    layers_to_unhide = []
    for prefix in ["litnik", "Litnik", "Brnak", "brnak"]:
        layers_to_unhide.extend(toggle_layers_with_prefix(prefix))
    for i in range(178):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 1, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, i)
    for i in range(180):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 2, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, 180 + i)
    for i in range(45):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 0, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, 360 + i)
    for i in range(180):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 2, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, 405 + i)

    for layer in layers_to_unhide:
        rs.LayerVisible(layer, True)


##################################################################################################
## READING CONFIG TO GET PYTHON_PATH
def get_python_path():
    """Read the configuration file and return the Python path."""

    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("PYTHON_PATH="):
                return line.strip().split('=')[1]
    return None

##################################################################################################
## READING CONFIG TO GET CREATE_VIDEO_WITH_LOGO_PATH
def get_create_video_python_file_path():
    """Read the configuration file and return the Python path."""

    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("CREATE_VIDEO_WITH_LOGO_PATH="):
                return line.strip().split('=')[1]
    return None

##################################################################################################
## READING CONFIG TO GET CALCULATE_WEIGHT_FILE_PATH
def get_calculate_weight_file_path():
    """Read the configuration file and return the path."""

    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("CALCULATE_WEIGHT_PATH="):
                return line.strip().split('=')[1]
    return None

##################################################################################################
## READING CONFIG TO GET CREATE_STONE_MAP_PATH
def get_create_stone_map_path():
    """Read the configuration file and return the path."""

    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("CREATE_STONE_MAP_PATH="):
                return line.strip().split('=')[1]
    return None

##################################################################################################
## ALLIGN ALL OBJECTS
def align_all():
    rs.SelectObjects(rs.AllObjects())
    all_objects = rs.AllObjects()
    if len(all_objects) > 1:
        rs.Command("_Group")
    rs.Command("_Align _Concentric _Enter")
    rs.UnselectAllObjects()

def rotate90():
    rs.SelectObjects(rs.AllObjects())
    rs.Command("_Rotate 0 90 _Enter")

def rotate180():
    rs.SelectObjects(rs.AllObjects())
    rs.Command("_Rotate 0 180 _Enter")


##################################################
# Creating Stone Map functions Start

def get_gem_data():
    block_instances = rs.ObjectsByType(rs.filter.instance)

    gem_data, total_carat_weight = measureGems(block_instances)
    if gem_data:
        gem_data = format_gem_data(gem_data, total_carat_weight)
        return gem_data
    return ""

def measureGems(gems):
    gemDict = {}
    unique_gems = {}

    for gem in gems:
        xform = rs.BlockInstanceXform(gem)
        plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)
        box = rs.BoundingBox(gem, plane, True)
        if box:
            width = round(rs.Distance(box[0], box[1]), 2)
            length = round(rs.Distance(box[0], box[3]), 2)
            height = round(rs.Distance(box[0], box[4]), 2)
            key = (length, width, height)
            if key in gemDict:
                gemDict[key] += 1
            else:
                gemDict[key] = 1
                unique_gems[key] = gem

    total_carat_weight = calculate_total_carat_weight(gemDict, unique_gems)
    return gemDict, total_carat_weight

def format_gem_data(gem_data, total_carat_weight):
    output = "\n"
    total_count = 0
    for dimensions, count in gem_data.items():
        length, width = dimensions[:2]
        if count == 1:
            output += "{}x{}: 1 stone\n".format(length, width)
        else:
            output += "{}x{}: {} stones\n".format(length, width, count)
        total_count += count
    output += ("\nTotal number of stones: {}\n".format(total_count))
    output += ("Total carat weight: {:.2f} carats\n".format(total_carat_weight))

    return output

def calculate_total_carat_weight(gemDict, unique_gems):
    total_volume_mm3 = 0

    for key, gem in unique_gems.items():
        # Copy the block instance
        copied_gem = rs.CopyObject(gem)
        if not copied_gem:
            continue

        # Explode the copied block instance to get individual components
        exploded_objects = rs.ExplodeBlockInstance(copied_gem)
        if not exploded_objects:
            rs.DeleteObject(copied_gem)
            continue

        volume_mm3 = 0
        for obj in exploded_objects:
            volume_data = rs.SurfaceVolume(obj)
            if not volume_data:  # Try as mesh if surface volume is None
                volume_data = rs.MeshVolume(obj)
            if volume_data:
                volume_mm3 += volume_data[0]

        # Clean up exploded objects
        rs.DeleteObjects(exploded_objects)
        rs.DeleteObject(copied_gem)

        # Multiply the volume by the number of identical gems
        total_volume_mm3 += volume_mm3 * gemDict[key]

    total_volume_cm3 = total_volume_mm3 * 1e-3  # Convert cubic millimeters to cubic centimeters

    density = 3.52  # Density of diamond in grams per cubic centimeter
    total_mass_grams = total_volume_cm3 * density  # Calculate total mass in grams

    total_carat_weight = total_mass_grams / 0.2  # Convert mass to carats (1 carat = 0.2 grams)

    return total_carat_weight

##################################################
# Creating Stone Map functions End
