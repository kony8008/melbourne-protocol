"""
MELBOURNE PROTOCOL - Phase 3: Materials & Lighting
Applies realistic materials and late-afternoon lighting to the city.
Includes:
- Glass-blue/grey facade materials on CBD buildings with per-building variation
- Green material on MCG field
- Blue-grey water material on Yarra River
- Dark asphalt on ground plane
- Emissive warm window strips on Eureka Tower gold top
- Sun light + fill light for golden hour aesthetic

Idempotent: assumes Melbourne collection exists with Phase 1 & 2 objects.
"""

import bpy
import random

def setup_world_lighting():
    """Configure world background for late-afternoon sunset."""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg_node = world.node_tree.nodes["Background"]
    bg_node.inputs[0].default_value = (0.95, 0.75, 0.55, 1.0)  # Warm sunset orange
    bg_node.inputs[1].default_value = 1.2  # Strength

def add_sun_light():
    """Add directional sun light for golden hour."""
    bpy.ops.object.light_add(type='SUN', location=(50, 50, 80))
    sun = bpy.context.active_object
    sun.name = "SunLight"
    sun.data.energy = 2.5
    sun.data.angle = 0.05
    sun.data.color = (1.0, 0.9, 0.7)  # Warm golden
    return sun

def add_fill_light():
    """Add soft blue ambient fill light."""
    bpy.ops.object.light_add(type='AREA', location=(-60, -60, 60))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 0.8
    fill.data.color = (0.5, 0.7, 1.0)  # Soft blue
    fill.data.size = 100
    return fill

def apply_cbd_materials(collection):
    """Apply glass-blue facade materials to CBD buildings with variation."""
    random.seed(42)  # Deterministic variation
    
    for obj in collection.objects:
        if obj.name.startswith("Bldg_"):
            obj.data.materials.clear()
            
            mat = bpy.data.materials.new(name=f"GlassFacade_{obj.name}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            
            # Per-building hue variation: blue-grey to blue-green
            base_color = (
                0.4 + random.uniform(-0.1, 0.1),
                0.5 + random.uniform(-0.05, 0.1),
                0.7 + random.uniform(-0.1, 0.05),
                1.0
            )
            bsdf.inputs[0].default_value = base_color
            bsdf.inputs[26].default_value = 0.3  # Metallic for glass reflection
            bsdf.inputs[2].default_value = 0.1   # Slight roughness
            
            obj.data.materials.append(mat)

def apply_mcg_material(collection):
    """Apply bright grass green material to MCG field."""
    for obj in collection.objects:
        if obj.name == "MCG_Field":
            obj.data.materials.clear()
            mat = bpy.data.materials.new(name="MCG_GreenField")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs[0].default_value = (0.15, 0.55, 0.15, 1.0)  # Bright grass
            bsdf.inputs[2].default_value = 0.6  # Roughness for grass
            obj.data.materials.append(mat)

def apply_yarra_material(collection):
    """Apply blue-grey water material to Yarra River."""
    for obj in collection.objects:
        if obj.name == "YarraRiver":
            obj.data.materials.clear()
            mat = bpy.data.materials.new(name="WaterMaterial")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs[0].default_value = (0.15, 0.35, 0.45, 0.9)  # Blue-grey
            bsdf.inputs[2].default_value = 0.2  # Smooth water
            bsdf.inputs[26].default_value = 0.4  # Metallic reflection
            obj.data.materials.append(mat)

def apply_ground_material(collection):
    """Apply dark asphalt material to ground plane."""
    for obj in collection.objects:
        if obj.name == "GroundPlane":
            obj.data.materials.clear()
            mat = bpy.data.materials.new(name="AsphaltGround")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs[0].default_value = (0.15, 0.15, 0.15, 1.0)  # Dark asphalt
            bsdf.inputs[2].default_value = 0.7  # Rough asphalt
            obj.data.materials.append(mat)

def apply_eureka_top_emissive(collection):
    """Apply emissive warm window strips to Eureka Tower gold top."""
    for obj in collection.objects:
        if obj.name == "EurekaTower_GoldTop":
            obj.data.materials.clear()
            mat = bpy.data.materials.new(name="GoldTopEmissive")
            mat.use_nodes = True
            tree = mat.node_tree
            
            # Clear default nodes
            tree.nodes.clear()
            
            # Create shader nodes
            bsdf = tree.nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf.inputs[0].default_value = (1.0, 0.84, 0.0, 1.0)  # Gold
            bsdf.inputs[26].default_value = 0.8  # Metallic
            
            emission = tree.nodes.new(type='ShaderNodeEmission')
            emission.inputs[0].default_value = (1.0, 0.8, 0.3, 1.0)  # Warm glow
            emission.inputs[1].default_value = 1.5  # Strength
            
            add_shader = tree.nodes.new(type='ShaderNodeAddShader')
            output = tree.nodes.new(type='ShaderNodeOutputMaterial')
            
            # Connect: BSDF + Emission -> Add -> Output
            tree.links.new(bsdf.outputs[0], add_shader.inputs[0])
            tree.links.new(emission.outputs[0], add_shader.inputs[1])
            tree.links.new(add_shader.outputs[0], output.inputs[0])
            
            obj.data.materials.append(mat)

def main():
    """Main execution."""
    print("\n=== MELBOURNE PROTOCOL - Phase 3: Materials & Lighting ===\n")
    
    # Get Melbourne collection
    if "Melbourne" not in bpy.data.collections:
        print("ERROR: Melbourne collection not found. Run phases 1 & 2 first.")
        return
    
    collection = bpy.data.collections["Melbourne"]
    
    # Setup world and lights
    print("Setting up world lighting (sunset sky)...")
    setup_world_lighting()
    
    print("Adding sun light (golden hour)...")
    add_sun_light()
    
    print("Adding fill light (soft blue)...")
    add_fill_light()
    
    # Apply materials
    print("Applying glass-blue facade materials to CBD buildings...")
    apply_cbd_materials(collection)
    
    print("Applying green material to MCG field...")
    apply_mcg_material(collection)
    
    print("Applying water material to Yarra River...")
    apply_yarra_material(collection)
    
    print("Applying asphalt material to ground plane...")
    apply_ground_material(collection)
    
    print("Applying emissive material to Eureka Tower gold top...")
    apply_eureka_top_emissive(collection)
    
    print(f"\n✓ Phase 3 complete: Materials & lighting applied")
    print(f"  - World: sunset sky (0.95, 0.75, 0.55)")
    print(f"  - Sun: warm golden hour (2.5 energy)")
    print(f"  - Fill: soft blue ambient (0.8 energy)")
    print(f"  - CBD: glass-blue facades with per-building variation")
    print(f"  - MCG: bright grass green")
    print(f"  - Yarra: blue-grey water with reflection")
    print(f"  - Ground: dark asphalt")
    print(f"  - Eureka top: emissive warm gold")

if __name__ == "__main__":
    main()
