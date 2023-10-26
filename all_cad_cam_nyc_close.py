import rhinoscriptsyntax as rs
import Rhino as rh
import Rhino.Render as rr
import Rhino.DocObjects as rd
import scriptcontext as sc
import os

def toggle_layers_with_prefix(prefix, action="hide"):
    """Toggle visibility of layers with a given prefix."""
    layers = [l for l in rs.LayerNames() if l.startswith(prefix)]
    
    if action == "hide":
        return [l for l in layers if rs.LayerVisible(l, False)]
    elif action == "show":
        [rs.LayerVisible(l, True) for l in layers]
        return []

def export_current_to_stl():
    """Export current Rhino doc to STL."""
    doc_path, doc_name = rs.DocumentPath(), rs.DocumentName()
    
    if not (doc_path and doc_name):
        print("Please save your Rhino file first.")
        return

    directory = os.path.dirname(doc_path)
    stl_filename = os.path.join(directory, os.path.splitext(doc_name)[0] + ".stl")
    
    layers_to_unhide = []
    for prefix in ["Gem", "CADRAWS", "Cutting"]:
        layers_to_unhide.extend(toggle_layers_with_prefix(prefix))

    rs.SelectObjects(rs.AllObjects())
    rs.Command('-_Export "{}" _ExportFileAs=_Binary _Enter _Enter'.format(stl_filename))
    #rs.Command('_-Export "{}" _Enter _Enter'.format(filename), False)
    #rs.Command('_Export "{}" _Enter'.format(stl_filename), False)
    #rs.Command('_-Export "{}" _ExportFileAs=ASCII _Enter _PolygonDensity=50 _Enter'.format(stl_filename), False)
    rs.UnselectAllObjects()

    for layer in layers_to_unhide:
        rs.LayerVisible(layer, True)
    
    rs.Command("_ZEA")
    
    if os.path.exists(stl_filename):
        os.startfile(stl_filename)
        
##################################################################

def remove_all_materials():
    """Remove all materials from the document."""
    mats = [mat for mat in sc.doc.Materials]
    for mat in mats:
        sc.doc.Materials.Remove(mat)
    
    rms = [rm for rm in sc.doc.RenderMaterials]
    for rm in rms:
        sc.doc.RenderMaterials.Remove(rm)

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


def select_objects_in_gem_layers_and_assign_material(material_name):
    """Select objects in 'Gem' layers and assign a specified material."""
    gem_layers = [layer for layer in rs.LayerNames() if layer.startswith("Gem")]
    for layer in gem_layers:
        objs = rs.ObjectsByLayer(layer)
        if objs:
            rs.SelectObjects(objs)
    if rs.SelectedObjects():
        rs.Command('_RenderAssignMaterialToObjects "{}"'.format(material_name), False)
    rs.UnselectAllObjects()
        
def select_objects_not_in_gem_layers_and_assign_material(material_name):
    """Select objects not in 'Gem' layers and assign a specified material."""
    all_layers = rs.LayerNames()
    non_gem_layers = [layer for layer in all_layers if not layer.startswith("Gem")]
    
    for layer in non_gem_layers:
        objs = rs.ObjectsByLayer(layer)
        if objs:
            rs.SelectObjects(objs)
    
    if rs.SelectedObjects():
        rs.Command('_RenderAssignMaterialToObjects "{}"'.format(material_name), False)
    rs.UnselectAllObjects()
    
#######################################################################
    
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

def set_display_mode_for_all_views(mode):
    """Sets the display mode for all views."""
    for view in rs.ViewNames():
            rs.ViewDisplayMode(view, mode)

def capture_current_view(directory, view_name, width=1118, height=627):
    """Captures the current view and saves it to the specified directory."""
    capture_path = os.path.join(directory, "{}.png".format(view_name))
    rs.Command('-ViewCaptureToFile "{}" Width={} Height={} Enter'.format(capture_path, width, height), False)

def capture_all_views(directory_base):
    """Captures all views and saves them to the specified directory."""
    current_view = rs.CurrentView()
    set_display_mode_for_all_views("CADCAMNYC")

    for view in rs.ViewNames():
        rs.CurrentView(view)
        if view != "Perspective":
            capture_current_view(directory_base, view)

    custom_views = [("Isometric", "_NE"), ("Isometric", "_SE")]
    for view_name, command in custom_views:
        rs.Command("_" + view_name + " " + command)
        capture_current_view(directory_base, view_name + "_" + command)
    rs.Command("_Right")
    set_display_mode_for_all_views("Shaded")
    rs.ViewDisplayMode("Perspective", "Rendered")
    rs.CurrentView(current_view)

    
##############################################################


def main():
    
    #################################################
    
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    export_current_to_stl()
    
    ##########################################

    remove_all_materials()

    # Create materials
    create_pbr_material(rh.Display.Color4f.FromArgb(255, 0.953, 0.815, 0.564), "Gold")
    create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 1, 1), "Silver")
    create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 1, 1), "Diamond", opacity=0)
    create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 0.749, 0.749), "Ruby", opacity=0)
    rs.Command("_ZEA")
    rs.Command("-DocumentProperties R B B 105,105,105 enter enter enter", False)

    select_objects_not_in_gem_layers_and_assign_material("Gold")
    select_objects_in_gem_layers_and_assign_material("Diamond")
    
  
    rs.Command("_ZEA")
    rs.Redraw()
    
    #######################################
    
    captures_directory = create_directory("Captures")
    if captures_directory:
        capture_all_views(captures_directory)
        
    ########################################
    

if __name__ == '__main__':
    main()
    sc.doc.Modified = False
    rs.Command("_Exit")