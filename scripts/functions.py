import rhinoscriptsyntax as rs
import Rhino as rh
import Rhino.Render as rr
import Rhino.DocObjects as rd
import scriptcontext as sc
import os

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
    rs.Command('-ViewCaptureToFile W 1024 H 567 Scale 1 "{}" Enter'.format(capture_path), False)

    
##################################################################################################
## CREATE VIDEO FROM CAPTURES
def create_video_captures(directory_base):
    for i in range(180):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 0, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, i)
    for i in range(180):
        viewPort = rs.CurrentView()
        rs.RotateView(viewPort, 2, 2)
        rs.RotateView(viewPort, 0, 2)
        rh.RhinoApp.Wait()
        capture_current_view(directory_base, 180 + i)

##################################################################################################
## READING CONFIG TO GET PYTHON_PATH
def get_python_path():
    """Read the configuration file and return the Python path."""

    base_path = rs.DocumentPath()

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

    base_path = rs.DocumentPath()

    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("CREATE_VIDEO_WITH_LOGO_PATH="):
                return line.strip().split('=')[1]
    return None