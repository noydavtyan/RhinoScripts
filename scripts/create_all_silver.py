import rhinoscriptsyntax as rs
import Rhino as rh
import scriptcontext as sc
import subprocess
import functions as functions
import os


def main():
    
    #################################################
    rs.CurrentView("Perspective")
    rs.Command("_SetView _World _Perspective")
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    functions.export_to_stl()
    
    ##########################################

    functions.remove_all_materials()

    # Create materials
    functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 1, 1), "Silver")
    functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 0.749, 0.749), "Ruby", opacity=0)
    rs.Command("_ZEA")
    rs.Command("-DocumentProperties R B B 105,105,105 enter enter enter", False)
    rs.Command("-DocumentProperties R B U BottomColor 105,105,105 Enter Enter Enter", False)
    rs.Command("-DocumentProperties R B U BottomColor 105,105,105 Enter Enter Enter", False)

    functions.select_objects_not_in_gem_layers_and_assign_material("Silver")
    functions.select_objects_in_gem_layers_and_assign_material("Ruby")
    
    rs.Command("_ZEA")
 
    rs.Redraw()
    
    #######################################
    
    rs.ViewDisplayMode("Perspective", "Rendered")
    rs.CurrentView("Perspective")
    captures_directory = functions.create_directory("Captures")
    if captures_directory:
        functions.create_video_captures(captures_directory)
        
    ########################################
    

if __name__ == '__main__':
    main()

    base_path = rs.DocumentPath()
    doc_name_with_extension = rs.DocumentName()

    # Split the name and extension, and take just the name part
    doc_name = os.path.splitext(doc_name_with_extension)[0]

    python_path = functions.get_python_path()
    create_video_python_path = functions.get_create_video_python_path()
    # Command to run the external Python script to add logos to all the images in the Captures folder
    command = [python_path,
            create_video_python_path,
            base_path, doc_name, "Captures"]

    # This will suppress the console window
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(command, startupinfo=startupinfo)

    sc.doc.Modified = False
    rs.Command("_Exit")


