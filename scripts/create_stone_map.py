import rhinoscriptsyntax as rs

def get_gem_data():
    block_instances = rs.ObjectsByType(rs.filter.instance)
    
    gem_data, total_carat_weight = measureGems(block_instances)
    if gem_data:
        format_gem_data(gem_data, total_carat_weight)

def measureGems(gems):
    gemDict = {}
    unique_gems = {}
    
    for gem in gems:
        xform = rs.BlockInstanceXform(gem)
        plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)
        box = rs.BoundingBox(gem, plane, True)
        if box:
            width = round(rs.Distance(box[0], box[1]), 2)
            length = round(rs.Distance(box[0], box[3]), 2)
            height = round(rs.Distance(box[0], box[4]), 2)
            key = (length, width, height)
            if key in gemDict:
                gemDict[key] += 1
            else:
                gemDict[key] = 1
                unique_gems[key] = gem
    
    total_carat_weight = calculate_total_carat_weight(gemDict, unique_gems)
    return gemDict, total_carat_weight

def format_gem_data(gem_data, total_carat_weight):
    total_count = 0
    for dimensions, count in gem_data.items():
        length, width = dimensions[:2]
        if count == 1:
            print("{}x{}: 1 stone".format(length, width))
        else:
            print("{}x{}: {} stones".format(length, width, count))
        total_count += count
    print("\nTotal number of stones: {}".format(total_count))
    print("Total carat weight: {:.2f} carats".format(total_carat_weight))

def calculate_total_carat_weight(gemDict, unique_gems):
    total_volume_mm3 = 0

    for key, gem in unique_gems.items():
        # Copy the block instance
        copied_gem = rs.CopyObject(gem)
        if not copied_gem:
            continue

        # Explode the copied block instance to get individual components
        exploded_objects = rs.ExplodeBlockInstance(copied_gem)
        if not exploded_objects:
            rs.DeleteObject(copied_gem)
            continue

        volume_mm3 = 0
        for obj in exploded_objects:
            volume_data = rs.SurfaceVolume(obj)
            if not volume_data:  # Try as mesh if surface volume is None
                volume_data = rs.MeshVolume(obj)
            if volume_data:
                volume_mm3 += volume_data[0]
        
        # Clean up exploded objects
        rs.DeleteObjects(exploded_objects)
        rs.DeleteObject(copied_gem)
        
        # Multiply the volume by the number of identical gems
        total_volume_mm3 += volume_mm3 * gemDict[key]
    
    total_volume_cm3 = total_volume_mm3 * 1e-3  # Convert cubic millimeters to cubic centimeters
    
    density = 3.52  # Density of diamond in grams per cubic centimeter
    total_mass_grams = total_volume_cm3 * density  # Calculate total mass in grams
    
    total_carat_weight = total_mass_grams / 0.2  # Convert mass to carats (1 carat = 0.2 grams)
    
    return total_carat_weight

def main():
    get_gem_data()

if __name__ == "__main__":
    main()
