import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc
import subprocess
import os

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    functions.export_to_stl()
    
    

if __name__ == '__main__':
    main()

    base_path = rs.DocumentPath()
    doc_name_with_extension = rs.DocumentName()

    # Split the name and extension, and take just the name part
    doc_name = os.path.splitext(doc_name_with_extension)[0]

    python_path = functions.get_python_path()
    calculate_weight_path = functions.get_calculate_weight_file_path()
    # Command to run the external Python script to add logos to all the images in the Captures folder
    command_calculate_weigth = [python_path,
            calculate_weight_path,
            base_path, doc_name]

    # This will suppress the console window
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(command_calculate_weigth, startupinfo=startupinfo)

    sc.doc.Modified = False
    rs.Command("_Exit")


