import rhinoscriptsyntax as rs
import Rhino as rh
import scriptcontext as sc
import subprocess
import functions as functions

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    all_layers = rs.LayerNames()
    for i in range(30):
        if str(i) in all_layers:
            functions.export_current_to_stl(i)
            functions.select_objects_in_layer(str(i))
            rs.Command("_Isolate")
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
            rs.Command("_Unisolate")

    
    

if __name__ == '__main__':
    main()

    # Get the path of the current script (as a replacement for the .bat file path)
    base_path = rs.DocumentPath()

    # Command to run the external Python script to add logos to all the images in the Captures folder
    command = ['C:/Users/noyda/AppData/Local/Programs/Python/Python37/python.exe', 
            'G:/Meine Ablage/3D Modelling/#s9hU_All_logos/add_logo_to_images.py',
            base_path]

    # This will suppress the console window
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(command, startupinfo=startupinfo)

    sc.doc.Modified = False
    rs.Command("_Exit")



