import rhinoscriptsyntax as rs
import Rhino as rh
import scriptcontext as sc
import subprocess
import functions as functions
import os

        
def main():
    rs.CurrentView("Perspective")
    rs.Command("_SetView _World _Perspective")
    rs.UnselectAllObjects()
    rs.Command("_ZEA")

    for i in range(30):
        rs.Command("_Unisolate")
        matching_layer_names = functions.select_all_objects_starting_with_number(i)
        rs.UnselectAllObjects()
        if len(matching_layer_names):
            for layer_name in matching_layer_names:
                functions.export_selected_layer_as_stl(layer_name, i)

            functions.select_all_objects_starting_with_number(i)
            rs.Command("_Isolate")
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

            parts = layer_name.split(str(i) + '_')
            layer_postfix = ('_' + parts[1]) if len(parts) > 1 else None

            rs.ViewDisplayMode("Perspective", "Rendered")
            rs.CurrentView("Perspective")
            captures_directory = functions.create_directory("Captures" + layer_postfix)
            if captures_directory:
                functions.create_video_captures(captures_directory)

            # Get the path of the current script (as a replacement for the .bat file path)
            base_path = rs.DocumentPath()
            # Get the full document name with extension
            doc_name_with_extension = rs.DocumentName()

            # Split the name and extension, and take just the name part
            doc_name = os.path.splitext(doc_name_with_extension)[0]
            # Command to run the external Python script to add logos to all the images in the Captures folder
            command = ['C:/Users/noyda/AppData/Local/Programs/Python/Python37/python.exe',
                    'G:/Meine Ablage/3D Modelling/#s9hU_All_logos/add_logo_to_images.py',
                    base_path, doc_name + layer_postfix, "Captures" + layer_postfix]

            # This will suppress the console window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.Popen(command, startupinfo=startupinfo)

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")

