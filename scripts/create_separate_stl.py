import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    all_layers = rs.LayerNames()
    for i in range(30):
        if str(i) in all_layers:
            functions.export_current_to_stl(i)
    
    

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")


