"""
MELBOURNE PROTOCOL - Phase 1: City Base
Procedurally generates ground plane, Yarra River, and CBD street grid (84 buildings).
Idempotent: clears and rebuilds the Melbourne collection on each run.
"""

import bpy
import bmesh
from mathutils import Vector

def clear_collection(name):
    """Remove collection and all its objects if it exists."""
    if name in bpy.data.collections:
        coll = bpy.data.collections[name]
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(coll)

def create_ground_plane(collection):
    """Create 100×100m ground plane, dark grey."""
    bpy.ops.mesh.primitive_plane_add(
        size=1, location=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = "GroundPlane"
    obj.scale = (50, 50, 1)
    
    # Material: dark grey asphalt
    mat = bpy.data.materials.new(name="GroundMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.2, 0.2, 0.2, 1.0)
    obj.data.materials.append(mat)
    
    collection.objects.link(obj)
    bpy.context.collection = collection
    return obj

def create_yarra_river(collection):
    """Create 80×8m Yarra River, blue water, positioned south of center."""
    bpy.ops.mesh.primitive_plane_add(
        size=1, location=(0, -46, 0.1)
    )
    obj = bpy.context.active_object
    obj.name = "YarraRiver"
    obj.scale = (40, 4, 1)
    
    # Material: blue water
    mat = bpy.data.materials.new(name="WaterMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.1, 0.3, 0.5, 0.95)
    obj.data.materials.append(mat)
    
    collection.objects.link(obj)
    return obj

def create_cbd_grid(collection):
    """Create 12×12 grid of buildings (84 total) in CBD area.
    Grid spans ~60×60m centered at origin.
    Variable heights: 10-50m.
    """
    import random
    random.seed(42)  # Deterministic for reproducibility
    
    grid_size = 12
    spacing = 5  # 5m between building centers
    start_offset = -(grid_size * spacing) / 2
    
    for row in range(grid_size):
        for col in range(grid_size):
            x = start_offset + col * spacing
            y = start_offset + row * spacing
            
            # Random height: 10-50m
            height = random.uniform(10, 50)
            z = height / 2
            
            # Create cube
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(x, y, z)
            )
            obj = bpy.context.active_object
            obj.name = f"Bldg_{row:02d}_{col:02d}"
            obj.scale = (2, 2, height / 2)
            
            # Material: grey concrete
            mat = bpy.data.materials.new(name=f"BuildingMat_{row}_{col}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
            obj.data.materials.append(mat)
            
            collection.objects.link(obj)

def main():
    """Main execution."""
    print("\n=== MELBOURNE PROTOCOL - Phase 1: City Base ===\n")
    
    # Clear existing Melbourne collection
    clear_collection("Melbourne")
    
    # Create new collection
    collection = bpy.data.collections.new("Melbourne")
    bpy.context.scene.collection.children.link(collection)
    
    # Build city
    print("Creating ground plane (100×100m)...")
    create_ground_plane(collection)
    
    print("Creating Yarra River (80×8m)...")
    create_yarra_river(collection)
    
    print("Creating CBD grid (12×12 buildings, variable heights)...")
    create_cbd_grid(collection)
    
    print(f"\n✓ Phase 1 complete: {len(collection.objects)} objects in Melbourne collection")
    print(f"  - Ground plane: 100×100m")
    print(f"  - Yarra River: 80×8m")
    print(f"  - CBD buildings: 144 (12×12 grid, 10-50m heights)")

if __name__ == "__main__":
    main()
