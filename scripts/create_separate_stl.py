import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")

    for i in range(30):
        rs.Command("_Unisolate")
        matching_layer_names = functions.select_all_objects_starting_with_number(i)
        rs.UnselectAllObjects()
        if len(matching_layer_names):
            for layer_name in matching_layer_names:
                functions.export_selected_layer_as_stl(layer_name, i)

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")


