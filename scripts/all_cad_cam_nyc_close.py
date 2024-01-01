import rhinoscriptsyntax as rs
import Rhino as rh
import Rhino.Render as rr
import Rhino.DocObjects as rd
import scriptcontext as sc
import subprocess
import os

    
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
    rs.Command('-ViewCaptureToFile Width={} Height={} "{}" Enter'.format(capture_path, width, height), False)

def capture_all_views(directory_base):
    """Captures all views and saves them to the specified directory."""
    current_view = rs.CurrentView()
    set_display_mode_for_all_views("CADCAMNYC")

    for view in rs.ViewNames():
        rs.CurrentView(view)
        if view != "Perspective":
            capture_current_view(directory_base, view)

    custom_views = [("Isometric", "_NE"), ("Isometric", "_SE"), ("Isometric", "_SW"), ("Isometric", "_NW")]
    for view_name, command in custom_views:
        rs.Command("_" + view_name + " " + command)
        capture_current_view(directory_base, view_name + "_" + command)
    rs.Command("_Right")
    set_display_mode_for_all_views("Shaded")
    rs.ViewDisplayMode("Perspective", "Rendered")
    rs.CurrentView(current_view)

    
##############################################################


def main():
    captures_directory = create_directory("Captures")
    if captures_directory:
        capture_all_views(captures_directory)
        
    ########################################
    

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")