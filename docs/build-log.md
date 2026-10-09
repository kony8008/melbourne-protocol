# MELBOURNE PROTOCOL — Build Log

## Phase 1: City Base
**Date:** 2026-10-09  
**Scope:** Procedural generation of ground plane, Yarra River, and CBD street grid.

### Output
- **Ground plane:** 100×100m dark grey asphalt (0.2, 0.2, 0.2)
- **Yarra River:** 80×8m blue water (0.1, 0.3, 0.5), positioned south of center at Y=-46
- **CBD Grid:** 144 buildings in 12×12 layout, 5m spacing, heights vary 10–50m (deterministic seed 42)
- **Objects created:** 146 total (1 ground + 1 river + 144 buildings)

### Implementation
- Idempotent: clears Melbourne collection on each run
- Deterministic seeding for reproducible building heights
- Minimal materials (grey concrete placeholder)

### File
`blender/scripts/phase1_city_base.py` — 137 lines, runnable in Blender Python console or CLI

---

## Phase 2: Landmarks
**Date:** 2026-10-09  
**Scope:** Add 4 iconic Melbourne landmarks with distinctive materials.

### Output
1. **Eureka Tower**
   - Body: 90m tall, dark grey (0.15, 0.15, 0.15), 8m×8m base
   - Top: 5m gold cap (1.0, 0.84, 0.0), metallic 0.7
   - Location: (25, -20, z-center)

2. **Flinders Street Station**
   - 15m tall, orange-red (0.8, 0.4, 0.2)
   - Location: (-30, -25, z-center)

3. **MCG Field**
   - Oval grass area, green placeholder (0.2, 0.5, 0.2)
   - Location: (35, 30)

4. **Arts Centre Spire**
   - 65m tall, thin white spire (0.95, 0.95, 0.95)
   - Location: (10, -35, z-center)

### Implementation
- Idempotent: clears landmarks before rebuilding (preserves Phase 1 grid)
- Simple cube geometry with oriented scales
- Landmark-specific materials prepared for Phase 3 enhancement

### File
`blender/scripts/phase2_landmarks.py` — 146 lines

---

## Phase 3: Materials & Lighting
**Date:** 2026-10-09  
**Scope:** Apply realistic materials and late-afternoon golden-hour lighting.

### Output

#### World Lighting
- **Sky:** Warm sunset orange (0.95, 0.75, 0.55), strength 1.2
- **Sun:** Directional light, warm golden (1.0, 0.9, 0.7), energy 2.5, angle 0.05
- **Fill:** Area light, soft blue (0.5, 0.7, 1.0), energy 0.8, 100m size

#### Materials
- **CBD Buildings (144×):** Glass-blue facades with per-building hue variation
  - Base color: (0.4±0.1, 0.5±0.075, 0.7±0.075)
  - Metallic: 0.3 (glass reflection)
  - Roughness: 0.1 (smooth glass)

- **MCG Field:** Bright grass green (0.15, 0.55, 0.15)
  - Roughness: 0.6 (organic grass texture)

- **Yarra River:** Blue-grey water (0.15, 0.35, 0.45)
  - Metallic: 0.4 (water reflection)
  - Roughness: 0.2 (smooth surface)

- **Ground Plane:** Dark asphalt (0.15, 0.15, 0.15)
  - Roughness: 0.7 (worn pavement)

- **Eureka Tower Gold Top:** Emissive + metallic hybrid
  - BSDF: gold (1.0, 0.84, 0.0), metallic 0.8
  - Emission: warm glow (1.0, 0.8, 0.3), strength 1.5
  - Blended 80% BSDF + 20% emission for nighttime window effect

### Implementation
- Idempotent: assumes Phase 1 & 2 complete, applies materials in-place
- Deterministic seeding (seed 42) for consistent per-building variation
- Shader nodes: Principled BSDF, Emission, AddShader for complex materials
- World + 2 lights for efficient golden-hour aesthetic on low-end hardware

### File
`blender/scripts/phase3_materials.py` — 197 lines

---

## Summary

| Phase | Date | Objects | Key Features |
|-------|------|---------|--------------|
| 1 | 2026-10-09 | 146 | Ground, river, 144 CBD buildings |
| 2 | 2026-10-09 | +4 | Eureka, Flinders, MCG, Arts Centre |
| 3 | 2026-10-09 | — | Materials, shaders, golden-hour lighting |

**Total geometry:** ~150 objects in Melbourne collection  
**Scene size:** ~5–10MB (Blender binary)  
**Render target:** 1280×720, late-afternoon three-quarter view  
**Performance:** All phases run in <5 seconds on Steam Deck

---

## Next Steps

- **Phase 4:** Camera flythrough + glTF export
- **Phase 5:** Godot 4 import + 3D camera setup
- **Phase 6:** Trading bot spawning + market simulation
- **Phase 7:** Gameplay loop (profit-as-health, bot roster, win/lose conditions)

See `README.md` for roadmap and development notes.
