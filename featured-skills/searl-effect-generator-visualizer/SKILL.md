---
name: searl-effect-generator-visualizer
description: Designs a real-time 3D visualization of John Searl's SEG (Searl Effect Generator) — concentric magnetic rotor rings, self-accelerating roller cylinders, radial magnetic wave patterns, and the hypothesized electron-spin plasma boundary layer. Invoke when asked to visualize the SEG, Searl Effect, magnetic rotor rings, or self-accelerating magnetic rollers in 3D.
---

# Searl Effect Generator (SEG) Visualizer

Produces a real-time 3D visualization of John Searl's SEG — three concentric magnetized rings (stator plates) surrounded by freely-rolling magnetized cylindrical rollers that self-accelerate via a magnetic waveform interaction, generating a surrounding electron-plasma boundary layer — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particle systems.

## When to Use

- User asks to visualize the SEG, Searl Effect Generator, or Searl's magnetic rotor rings
- User wants an animated 3D model of self-accelerating magnetic rollers and concentric ring stators
- A demonstration of rotating magnetic wave-interference patterns in 3D is needed
- User is building an educational or speculative-physics tool around Searl's free-energy claims
- User wants to render magnetic field patterns, plasma boundary layers, or self-organizing rotor dynamics

## Process

1. **Stator ring geometry**:
   - Model three concentric ring stators (inner, mid, outer) using `TorusGeometry` with increasing major radii (1.0, 1.8, 2.8) and a rectangular cross-section achieved via `ExtrudeGeometry` on a square profile curve
   - Each stator is composed of four bonded material layers (Nylon, Iron, Neodymium, Aluminium); represent these as `InstancedMesh` segments arranged in a ring, each rendered with a distinct `MeshStandardMaterial` color
   - Animate a traveling magnetic wave pattern along the stator surface using a `ShaderMaterial` with a `sin(uAngle − time·uWaveSpeed)` modulation on the `emissiveIntensity`

2. **Roller cylinder geometry**:
   - For each stator ring, instantiate `n` rollers (inner: 12, mid: 22, outer: 36) using `InstancedMesh` of `CylinderGeometry` (radius = stator cross-section height × 0.9)
   - Each roller orbits its stator ring at a self-accelerating angular velocity: `ω(t) = ω₀ · e^(α·t)` up to a clamped maximum, computed per-instance in the vertex shader via an `instanceOffset` attribute
   - Each roller also spins on its own axis (self-rotation) at a rate proportional to the stator wave speed — encode this as a second `quaternion` attribute updated each frame

3. **Magnetic wave interference pattern**:
   - On the stator surfaces, render the radial magnetic waveform as a `DataTexture` (RGBA32F) that encodes the superposition of each stator's pole pattern and the roller's induced field
   - Sample the texture in a `ShaderMaterial` to produce the characteristic Searl "magnetic wave" ripple texture — alternating bands of north/south polarity shown as blue/red
   - Animate the texture by advancing a phase offset uniform each frame

4. **Electron-plasma boundary layer**:
   - Spawn 100 000 particles (Three.js `Points`) orbiting just outside the outermost stator ring in a thin toroidal shell
   - Particles follow a near-circular orbit with a tangential drift velocity computed in the TSL vertex shader; add a small radial oscillation to simulate the "electron bounce" effect
   - Color particles by speed: slow outer fringe (deep violet) to fast inner boundary (white-gold)
   - Gradually increase particle orbital radius over time when `self_acceleration` is enabled — particles spiral outward as the SEG "spins up"

5. **Anti-gravity lift field**:
   - Render a downward-deflected "lift field" as 5 000 straight-line particles descending through the SEG disc plane, bending outward and upward at the device boundary (simulating the hypothesized dielectric/gravitational field displacement)
   - Use a TSL vertex shader that computes a curved path using a Bézier interpolation through three control points: below the device, at the rim, and outward-upward

6. **Post-processing**:
   - `Bloom` (threshold 0.2, intensity 2.2) for the plasma boundary and magnetic wave peaks
   - `Scanlines` to evoke the period of Searl's 1960s–1970s experiments
   - Subtle `ColorAverage` filter desaturation for the metallic ring geometry to contrast with the bright plasma layer

7. **Runtime controls (lil-gui)**:
   - `base_rpm` (100–10 000) — initial stator wave speed / roller orbital speed
   - `self_acceleration` (toggle) — enables exponential roller velocity growth
   - `plasma_density` (10k–200k) — boundary layer particle count
   - `ring_count` (1–3) — number of active stator rings
   - `roller_count_multiplier` (0.5–2×) — scales rollers per ring
   - Toggles: `show_magnetic_waves`, `show_plasma_layer`, `show_lift_field`, `show_material_layers`

## Output Format

```
SearlSEGScene/
├── SearlSEGScene.jsx
├── components/
│   ├── StatorRings.jsx          ← Concentric ring InstancedMesh segments
│   ├── RollerCylinders.jsx      ← InstancedMesh rollers with orbit + spin
│   ├── MagneticWavePattern.jsx  ← DataTexture wave interference shader
│   ├── PlasmaBoundaryLayer.jsx  ← Points + TSL toroidal orbit shader
│   ├── LiftField.jsx            ← Curved Bézier lift-field particles
│   └── PostFX.jsx
├── shaders/
│   ├── magneticWave.tsl.js     ← TSL stator wave modulation
│   ├── rollerOrbit.tsl.js      ← TSL self-accelerating roller kinematics
│   └── plasmaOrbit.tsl.js      ← TSL toroidal particle orbit
└── controls/gui.js
```

## Boundaries

- Do NOT present the SEG's free-energy or anti-gravity claims as verified physics — label all speculative effects clearly.
- The roller magnetic interaction and self-acceleration have not been independently replicated; visualize them as Searl's model, not an experimentally confirmed mechanism.
- Do NOT recreate geometry per frame — use `InstancedMesh` with matrix/attribute updates only.
- Do NOT use more than 3 dynamic shadow-casting lights.
