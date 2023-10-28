import rhinoscriptsyntax as rs
import functions as functions
import scriptcontext as sc

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    functions.export_current_to_stl()
    
    

if __name__ == '__main__':
    main()

    sc.doc.Modified = False
    rs.Command("_Exit")


