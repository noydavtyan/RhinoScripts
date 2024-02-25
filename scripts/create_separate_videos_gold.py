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
            layer_name = matching_layer_names[0]

            functions.select_all_objects_starting_with_number(i)
            rs.Command("_Isolate")
            functions.remove_all_materials()

            # Create materials
            functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 0.953, 0.815, 0.564), "Gold")
            functions.create_pbr_material(rh.Display.Color4f.FromArgb(255, 1, 1, 1), "Diamond", opacity=0)
            rs.Command("_ZEA")
            rs.Command("-DocumentProperties R B B 105,105,105 enter enter enter", False)
            rs.Command("-DocumentProperties R B U BottomColor 105,105,105 Enter Enter Enter", False)
            rs.Command("-DocumentProperties R B U BottomColor 105,105,105 Enter Enter Enter", False)
            functions.select_objects_not_in_gem_layers_and_assign_material("Gold")
            functions.select_objects_in_gem_layers_and_assign_material("Diamond")

            rs.Command("_ZEA")

            rs.Redraw()

            #######################################

            parts = layer_name.split(str(i) + '_')
            layer_postfix = ('_' + parts[1]) if len(parts) > 1 else None

            captures_directory = functions.create_directory("Captures" + layer_postfix)
            if captures_directory:
                functions.create_video_captures(captures_directory)

            # Get the path of the current script (as a replacement for the .bat file path)
            base_path = rs.DocumentPath()
            # Get the full document name with extension
            doc_name_with_extension = rs.DocumentName()

            # Split the name and extension, and take just the name part
            doc_name = os.path.splitext(doc_name_with_extension)[0]

            python_path = functions.get_python_path()
            create_video_python_path = functions.get_create_video_python_file_path()
            # Command to run the external Python script to add logos to all the images in the Captures folder
            command = [python_path,
                    create_video_python_path,
                    base_path, doc_name + layer_postfix, "Captures" + layer_postfix]

            # This will suppress the console window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.Popen(command, startupinfo=startupinfo)

if __name__ == '__main__':
    main()
    sc.doc.Modified = False
    rs.Command("_Exit")


