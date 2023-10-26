import rhinoscriptsyntax as rs
import functions as functions

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    
    functions.export_current_to_stl()
    
    

if __name__ == '__main__':
    main()

    rs.Command("_Exit")


