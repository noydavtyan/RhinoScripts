import rhinoscriptsyntax as rs
import functions as functions

        
def main():
    rs.UnselectAllObjects()
    rs.Command("_ZEA")
    all_layers = rs.LayerNames()
    for i in range(30):
        if str(i) in all_layers:
            functions.export_current_to_stl(i)
    
    

if __name__ == '__main__':
    main()

    rs.Command("_Exit")


