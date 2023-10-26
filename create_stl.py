import rhinoscriptsyntax as rs
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
    rs.UnselectAllObjects()

    for layer in layers_to_unhide:
        rs.LayerVisible(layer, True)
    
    rs.Command("_ZEA")
    
    if os.path.exists(stl_filename):
        os.startfile(stl_filename)
        


def main():
    
    #################################################
    
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    export_current_to_stl()
    
    

if __name__ == '__main__':
    main()

    rs.Command("_Exit")


