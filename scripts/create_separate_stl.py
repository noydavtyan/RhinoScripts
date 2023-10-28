import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    all_layers = rs.LayerNames()
    for i in range(30):
        layer_name = None
        if str(i) in all_layers:
            layer_name = str(i)
        # Check if there's a layer that starts with 'i + _'
        elif any(item.startswith(str(i) + '_') for item in all_layers):
            layer_name = next(item for item in all_layers if item.startswith(str(i) + '_'))
        
        if layer_name:
            functions.export_current_to_stl(layer_name, str(i))
    
    

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")


