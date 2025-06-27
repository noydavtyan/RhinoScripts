import rhinoscriptsyntax as rs
import scriptcontext as sc
import os

# Calculate scale factor between circumferences
def scale_factor(current_circ, target_circ):
    return target_circ / current_circ

# Read the diameter-derived circumference and source STL path
temp_file = os.path.join(os.getenv('TEMP'), 'RingSize.txt')
with open(temp_file, 'r') as file:
    lines = file.readlines()
    current_circ = float(lines[0].strip().replace(',', '.'))
    source_stl = lines[1].strip()
    base_dir = os.path.dirname(source_stl)

eu_dir = os.path.join(base_dir, "sizes_eu")
us_dir = os.path.join(base_dir, "sizes_us")

if not os.path.exists(eu_dir):
    os.makedirs(eu_dir)

if not os.path.exists(us_dir):
    os.makedirs(us_dir)

# EU sizes: 40-76 mm circumference
eu_sizes = list(range(40, 77))

# US ring size to inner circumference (mm)
us_size_map = {
    "3": 44.2, "3.5": 45.5, "4": 46.8, "4.5": 48.0, "5": 49.3,
    "5.5": 50.6, "6": 51.9, "6.5": 53.1, "7": 54.4, "7.5": 55.7,
    "8": 57.0, "8.5": 58.3, "9": 59.5, "9.5": 60.8, "10": 62.1,
    "10.5": 63.4, "11": 64.6, "11.5": 65.9, "12": 67.2,
    "12.5": 68.5, "13": 69.7, "13.5": 71.0
}

# Import STL file
def import_stl(path):
    rs.Command('-_Import "{}" _Enter'.format(path), False)
    return rs.LastCreatedObjects()

# Export scaled STL
def scale_and_export(objs, factor, export_path):
    rs.SelectObjects(objs)
    rs.ScaleObjects(objs, [0, 0, 0], [factor, factor, factor])
    rs.Command('-_Export "{}" _Enter _Enter'.format(export_path), False)
    rs.DeleteObjects(objs)

# Export EU sizes
for eu_circ in eu_sizes:
    objs = import_stl(source_stl)
    factor = scale_factor(current_circ, eu_circ)
    output_path = os.path.join(eu_dir, "{}.stl".format(eu_circ))
    scale_and_export(objs, factor, output_path)

# Export US sizes
for us_label, us_circ in us_size_map.items():
    objs = import_stl(source_stl)
    factor = scale_factor(current_circ, us_circ)
    output_path = os.path.join(us_dir, "{}.stl".format(us_label))
    scale_and_export(objs, factor, output_path)

print("Export complete.")
os.remove(temp_file)
sc.doc.Modified = False