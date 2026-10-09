"""
MELBOURNE PROTOCOL - Phase 2: Landmarks
Adds 4 key Melbourne landmarks to the city:
1. Eureka Tower (90m, dark grey + gold top)
2. Flinders Street Station (15m, ornate orange-red)
3. MCG Field (oval grass area)
4. Arts Centre Spire (65m, white)

Idempotent: assumes Melbourne collection exists, clears landmarks before rebuilding.
"""

import bpy
from mathutils import Vector

def clear_landmarks(collection):
    """Remove landmark objects if they exist."""
    landmark_names = ["EurekaTower_Body", "EurekaTower_GoldTop", 
                      "FlandersStation", "MCG_Field", "ArtsCentreSpire"]
    for name in landmark_names:
        for obj in collection.objects:
            if obj.name == name:
                bpy.data.objects.remove(obj, do_unlink=True)

def create_eureka_tower(collection):
    """Eureka Tower: 90m tall, dark grey body + gold top.
    Located southeast of CBD center.
    """
    # Main body: dark grey, 8m×8m base, 85m tall
    bpy.ops.mesh.primitive_cube_add(location=(25, -20, 42.5))
    body = bpy.context.active_object
    body.name = "EurekaTower_Body"
    body.scale = (4, 4, 42.5)
    
    mat_body = bpy.data.materials.new(name="EurekaTowerBody")
    mat_body.use_nodes = True
    bsdf = mat_body.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.15, 0.15, 0.15, 1.0)  # Dark grey
    body.data.materials.append(mat_body)
    
    collection.objects.link(body)
    
    # Gold top: 5m tall, 8m×8m
    bpy.ops.mesh.primitive_cube_add(location=(25, -20, 87.5))
    top = bpy.context.active_object
    top.name = "EurekaTower_GoldTop"
    top.scale = (4, 4, 2.5)
    
    mat_top = bpy.data.materials.new(name="EurekaTowerTop")
    mat_top.use_nodes = True
    bsdf = mat_top.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (1.0, 0.84, 0.0, 1.0)  # Gold
    bsdf.inputs[26].default_value = 0.7  # Metallic
    top.data.materials.append(mat_top)
    
    collection.objects.link(top)

def create_flinders_station(collection):
    """Flinders Street Station: 15m tall, ornate orange-red.
    Located southwest of CBD center.
    """
    bpy.ops.mesh.primitive_cube_add(location=(-30, -25, 7.5))
    obj = bpy.context.active_object
    obj.name = "FlandersStation"
    obj.scale = (6, 8, 7.5)
    
    mat = bpy.data.materials.new(name="FlandersStationMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.8, 0.4, 0.2, 1.0)  # Orange-red
    obj.data.materials.append(mat)
    
    collection.objects.link(obj)

def create_mcg_field(collection):
    """MCG (Melbourne Cricket Ground): Oval grass field.
    Located northeast of CBD center.
    """
    bpy.ops.mesh.primitive_plane_add(location=(35, 30, 0.05))
    obj = bpy.context.active_object
    obj.name = "MCG_Field"
    obj.scale = (12, 16, 1)  # Oval proportions
    
    mat = bpy.data.materials.new(name="MCG_GrassMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.2, 0.5, 0.2, 1.0)  # Grass green
    obj.data.materials.append(mat)
    
    collection.objects.link(obj)

def create_arts_centre_spire(collection):
    """Arts Centre Spire: 65m tall white spire.
    Located south-central, near Yarra River.
    """
    bpy.ops.mesh.primitive_cube_add(location=(10, -35, 32.5))
    obj = bpy.context.active_object
    obj.name = "ArtsCentreSpire"
    obj.scale = (1.5, 1.5, 32.5)  # Thin tall spire
    
    mat = bpy.data.materials.new(name="ArtsCentreSpireMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)  # White
    obj.data.materials.append(mat)
    
    collection.objects.link(obj)

def main():
    """Main execution."""
    print("\n=== MELBOURNE PROTOCOL - Phase 2: Landmarks ===\n")
    
    # Get Melbourne collection
    if "Melbourne" not in bpy.data.collections:
        print("ERROR: Melbourne collection not found. Run phase1_city_base.py first.")
        return
    
    collection = bpy.data.collections["Melbourne"]
    
    # Clear existing landmarks
    print("Clearing existing landmarks...")
    clear_landmarks(collection)
    
    # Build landmarks
    print("Creating Eureka Tower (90m, dark grey + gold top)...")
    create_eureka_tower(collection)
    
    print("Creating Flinders Street Station (15m, orange-red)...")
    create_flinders_station(collection)
    
    print("Creating MCG Field (oval grass)...")
    create_mcg_field(collection)
    
    print("Creating Arts Centre Spire (65m, white)...")
    create_arts_centre_spire(collection)
    
    print(f"\n✓ Phase 2 complete: 4 landmarks added")
    print(f"  - Eureka Tower: 90m (25, -20)")
    print(f"  - Flinders Station: 15m (-30, -25)")
    print(f"  - MCG Field: oval (35, 30)")
    print(f"  - Arts Centre Spire: 65m (10, -35)")

if __name__ == "__main__":
    main()
