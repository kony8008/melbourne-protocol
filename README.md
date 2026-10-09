# MELBOURNE PROTOCOL

A stylized 3D survival-city trading game set in a cyberpunk-themed Melbourne. Solo developer, Steam Deck target, built with Blender (procedural geometry) and Godot 4.

## Current State

### Blender Scene (`assets/melbourne_city.blend`)
The scene contains a procedurally-generated low-poly Melbourne CBD with:

**Phase 1 — City Base:**
- Ground plane: 100×100m dark asphalt
- Yarra River: 80×8m blue water (south of center)
- CBD street grid: 144 buildings in 12×12 grid, variable heights 10–50m

**Phase 2 — Landmarks:**
- **Eureka Tower**: 90m dark grey + gold emissive top (southeast CBD at 25, -20)
- **Flinders Street Station**: 15m orange-red ornate building (southwest at -30, -25)
- **MCG Field**: Oval grass area (northeast at 35, 30)
- **Arts Centre Spire**: 65m white spire (south-central at 10, -35)

**Phase 3 — Materials & Lighting:**
- CBD buildings: glass-blue/grey facades with per-building hue variation
- MCG field: bright grass green (0.15, 0.55, 0.15)
- Yarra River: blue-grey water (0.15, 0.35, 0.45) with metallic reflection
- Ground plane: dark asphalt (0.15, 0.15, 0.15)
- Eureka gold top: emissive warm window strips (1.0, 0.8, 0.3)
- World: sunset sky (0.95, 0.75, 0.55)
- Lighting: Sun (warm golden hour, 2.5 energy) + Fill (soft blue, 0.8 energy)

## Running the Scripts

Each phase is a standalone, idempotent Python script. Run them in order in Blender.

### Option A: Blender UI (Scripting Tab)
1. Open Blender
2. Switch to **Scripting** workspace
3. Open script: `blender/scripts/phase1_city_base.py`
4. Click **Run Script** (or Alt+P)
5. Repeat for phase2 and phase3

### Option B: Command Line
```bash
# Run all phases in sequence
blender --background --python blender/scripts/phase1_city_base.py
blender --background --python blender/scripts/phase2_landmarks.py
blender --background --python blender/scripts/phase3_materials.py

# Or save to a new file
blender --background --python blender/scripts/phase1_city_base.py -- --save assets/melbourne_city.blend
```

### Option C: Within Blender Python Console
```python
exec(open("blender/scripts/phase1_city_base.py").read())
exec(open("blender/scripts/phase2_landmarks.py").read())
exec(open("blender/scripts/phase3_materials.py").read())
```

## File Structure

```
melbourne-protocol/
├── blender/
│   └── scripts/
│       ├── phase1_city_base.py       (Ground, Yarra, 144 CBD buildings)
│       ├── phase2_landmarks.py       (Eureka, Flinders, MCG, Arts Centre)
│       └── phase3_materials.py       (Materials, lighting, shaders)
├── docs/
│   └── build-log.md                  (Phase summary with dates)
├── exports/
│   └── (glTF, FBX, or other exports go here)
├── assets/
│   └── melbourne_city.blend          (Blender scene file, ~5–10MB)
├── README.md                         (This file)
└── .gitignore

```

## Asset Location

**Current save:** `/home/deck/Documents/melbourne_city.blend` (original working file)  
**Repo copy:** `assets/melbourne_city.blend` (copy for version control)

The `.blend` file is tracked in git (under 100MB). To export for Godot:
```bash
blender --background assets/melbourne_city.blend --python -c "
import bpy
bpy.ops.export_scene.gltf(filepath='exports/melbourne.glb', use_draco_compression=True)
"
```

## Roadmap

### Phase 4: Camera Flythrough & Export
- [ ] Create smooth camera path (orbit → landmarks → river follow)
- [ ] Render 240-frame animation (10 sec @ 24fps)
- [ ] Export as `.glb` (glTF) for Godot import

### Phase 5: Godot Integration
- [ ] Import `.glb` into Godot 4 scene
- [ ] Set up 3D camera controller (freelook or fixed angles)
- [ ] Implement trading bot spawning and pathfinding

### Phase 6: Market System
- [ ] Market tick simulation (Timer node + RNG)
- [ ] Order book UI (buy/sell orders for 3–5 assets)
- [ ] Profit/loss tracking (bot "health" system)

### Phase 7: Gameplay Loop
- [ ] Bot roster management (gatherer + trader classes)
- [ ] Resource collection (energy, data)
- [ ] Win/lose conditions (profitability thresholds)

## Development Notes

- **Target:** 60fps on Steam Deck integrated graphics (low-poly, instancing, no per-frame pathfinding)
- **Engine:** Godot 4 (GDScript)
- **Geometry:** Procedural in Blender, exported as glTF
- **Performance:** Prefer systems cheap to simulate (bot swarms via instancing, not individual pathfinding)
- **Art:** Stylized low-poly with neon cyberpunk overlay (night-only, wet-road reflections)

## Contributing

Scripts are idempotent and deterministic (seeded RNG). To modify:
1. Edit the relevant phase script
2. Run it in Blender to preview
3. Commit changes with a clear message

## License

TBD

---

**Last updated:** 2026-10-09  
**Maintainer:** Solo developer on Steam Deck
