import rhinoscriptsyntax as rs
import Rhino as rh
import scriptcontext as sc
import subprocess
import functions as functions


def main():
    
    #################################################
    rs.CurrentView("Perspective")
    rs.Command("_SetView _World _Perspective")
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    functions.export_current_to_stl()
    
    ##########################################

    functions.remove_all_materials()

    # Create materials
    functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 1, 1), "Silver")
    functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 0.749, 0.749), "Ruby", opacity=0)
    rs.Command("_ZEA")
    rs.Command("-DocumentProperties R B B 105,105,105 enter enter enter", False)

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

    # Get the path of the current script (as a replacement for the .bat file path)
    base_path = rs.DocumentPath()
    doc_name = rs.DocumentName()
    # Command to run the external Python script to add logos to all the images in the Captures folder
    command = ['C:/Users/noyda/AppData/Local/Programs/Python/Python37/python.exe', 
            'G:/Meine Ablage/3D Modelling/#s9hU_All_logos/add_logo_to_images.py',
            base_path, doc_name]

    # This will suppress the console window
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(command, startupinfo=startupinfo)

    sc.doc.Modified = False
    rs.Command("_Exit")


