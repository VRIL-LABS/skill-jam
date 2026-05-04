---
name: hutchison-effect-visualizer
description: Designs a real-time 3D visualization of the Hutchison Effect — overlapping RF, microwave, and Tesla coil interference field patterns producing anomalous material behaviors (levitation, jellification, transmutation zones) rendered as volumetric field interaction regions. Invoke when asked to visualize the Hutchison Effect, RF/microwave interference fields, or anomalous field-matter interaction zones in 3D.
---

# Hutchison Effect Visualizer

Produces a real-time 3D visualization of the Hutchison Effect — the anomalous material behaviors (levitation, molecular disruption, transmutation) reported by John Hutchison when overlapping multiple RF sources, Tesla coil fields, and static electric fields interfere constructively in a localized volume — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particles.

## When to Use

- User asks to visualize the Hutchison Effect, RF interference fields, or anomalous field interactions
- User wants a 3D rendering of overlapping electromagnetic field interference zones
- An interactive demonstration of constructive/destructive RF field superposition is needed
- User is building an educational or speculative-physics tool around John Hutchison's experiments
- User wants to render volumetric wave interference, levitation anomaly zones, or field-matter coupling visualizations

## Process

1. **Laboratory scene geometry**:
   - Model a simplified lab table as a `BoxGeometry` base plane
   - Place 4–6 RF emitters (small `CylinderGeometry` antenna stubs), one Tesla coil (a `TorusGeometry` top-load on a cylindrical secondary coil), and one Van de Graaff-style static sphere (`SphereGeometry`) around the table
   - Each emitter has a distinct color-coded `MeshStandardMaterial` to allow visual identification of each field source

2. **Multi-source field interference volume**:
   - Compute the superposed electric field amplitude at each point in a 3D grid as the sum of oscillating spherical wave contributions from each source:
     `E_total(r,t) = Σ_i (A_i / |r − r_i|) · sin(2π·f_i·t − k_i·|r − r_i|)`
   - Bake a 3D `DataTexture` (resolution 64³, RGBA32F) with the RMS interference pattern; update it on the GPU via a WebGPU compute shader (TSL `Fn()`) if available, or a WebGL render-target ping-pong
   - Raymarch this 3D texture in a fullscreen `ShaderMaterial` to render the volumetric interference field as a glowing fog

3. **Constructive interference "hot zone" visualization**:
   - Identify voxels in the 3D texture where `|E_total| > threshold` — these are the Hutchison "active zones"
   - Render each hot zone as a glowing, semi-transparent `SphereGeometry` with radius proportional to zone intensity, using an emissive `ShaderMaterial`
   - Animate the zones flickering with `Bloom`-amplified noise pulses to simulate the irregular, irreproducible nature of the effect

4. **Levitation anomaly simulation**:
   - Place 5–10 small object `BoxGeometry`/`SphereGeometry` props on the table surface
   - When a hot zone overlaps with an object, animate it rising (translating upward), wobbling (random rotation via Perlin noise), or deforming (vertex displacement via a `ShaderMaterial` noise function)
   - All object animations are driven by the interference field value at the object's position — sampled from the `DataTexture` and passed as a per-object uniform

5. **Tesla coil discharge arcs**:
   - Render stochastic electrical arcs from the Tesla coil top-load as procedural `TubeGeometry` paths generated each frame
   - Arc paths are computed via a random-walk lightning algorithm: start at top-load, step in direction of maximum field gradient + Gaussian noise, render as a `TubeGeometry` with `MeshBasicMaterial({ emissive: 0xffffff })`
   - Limit to 3–5 arcs per frame, each lasting 2–5 frames before regeneration

6. **Spectral field frequency overlay**:
   - Show a 2D frequency-domain display (waterfall plot style) as a `PlaneGeometry` + `ShaderMaterial` rendering a rolling spectrogram of the superposed fields
   - Color-map: low amplitude (deep blue) → high amplitude (white)

7. **Post-processing**:
   - `Bloom` (threshold 0.1, intensity 3.5) for arcs, hot zones, and emitters
   - `GodRays` from the Tesla coil top-load
   - `Glitch` (subtle, occasional) to evoke the chaotic, hard-to-reproduce nature of the effect

8. **Runtime controls (lil-gui)**:
   - `source_count` (2–6) — number of active RF/field sources
   - `frequencies` (array, 1 MHz–1 GHz each) — each source's operating frequency
   - `interference_threshold` (0.1–0.9) — hot-zone activation threshold
   - `tesla_coil_power` (0–1) — scales Tesla coil discharge arc frequency
   - `levitation_sensitivity` (0–1) — threshold for object levitation animation
   - Toggles: `show_field_volume`, `show_hot_zones`, `show_arcs`, `show_spectrogram`

## Output Format

```
HutchisonEffectScene/
├── HutchisonEffectScene.jsx
├── components/
│   ├── LabTable.jsx              ← Table + emitter/coil geometry
│   ├── FieldInterferenceVolume.jsx ← 3D DataTexture raymarched fog
│   ├── HotZones.jsx              ← Emissive SphereGeometry active zones
│   ├── LevitatingObjects.jsx     ← Field-driven object animation
│   ├── TeslaArcs.jsx             ← Procedural TubeGeometry arcs
│   ├── SpectralWaterfall.jsx     ← Rolling spectrogram display
│   └── PostFX.jsx
├── shaders/
│   ├── fieldInterference.tsl.js ← TSL superposed spherical wave sum
│   ├── volumeRaymarch.tsl.js    ← TSL 3D texture raymarch
│   └── lightningArc.js          ← JS random-walk arc path generator
└── controls/gui.js
```

## Boundaries

- Do NOT present the Hutchison Effect as reproducible, peer-reviewed science — it is John Hutchison's privately documented experimental claim; label all anomalous effects as such.
- Do NOT suggest the visualization can guide real high-power RF experiments — high-power RF and Tesla coils are dangerous; include a disclaimer.
- Do NOT recreate geometry per frame for stable objects; only regenerate the stochastic Tesla arc tubes each frame.
- The 3D interference volume computation is computationally intensive — always fall back to a lower-resolution `DataTexture` on low-end hardware, detected via `renderer.capabilities`.
