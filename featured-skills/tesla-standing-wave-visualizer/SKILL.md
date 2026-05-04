---
name: tesla-standing-wave-visualizer
description: Designs a real-time 3D visualization of Nikola Tesla's longitudinal standing waves and Wardenclyffe resonance system — Earth-resonance cavity modes, radial electric field pulses, ground-return currents, and the magnifying transmitter's toroidal field structure. Invoke when asked to visualize Tesla's wireless energy transmission, longitudinal waves, Wardenclyffe tower, or Earth-ionosphere resonance in 3D.
---

# Tesla Standing Wave Visualizer

Produces a real-time 3D visualization of Nikola Tesla's longitudinal standing wave and Earth-resonance system — the magnifying transmitter's toroidal field, ground-return current sheets, ionospheric reflection nodes, and radial electric field pulses — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particle systems.

## When to Use

- User asks to visualize Tesla's standing waves, longitudinal wave transmission, or Wardenclyffe resonance
- User wants a 3D model of Earth-ionosphere cavity resonance (Schumann-adjacent modes)
- An animated demonstration of radial electric field pulses propagating through the Earth is needed
- User is building an educational tool around Tesla's wireless energy transmission concepts
- User wants to render toroidal electromagnetic field structures or ground-return current flows in 3D

## Process

1. **Earth globe and ionosphere geometry**:
   - Render the Earth as a `SphereGeometry` (radius 2, segments 64) with a `MeshStandardMaterial` using an equirectangular Earth texture or a procedural `ShaderMaterial` with Simplex noise continents
   - Add an ionosphere shell as a slightly larger semi-transparent `SphereGeometry` (radius 2.15) with `MeshBasicMaterial({ transparent: true, opacity: 0.12, color: 0x88aaff, side: THREE.BackSide })`
   - Place the Wardenclyffe tower at a geographic coordinate on the Earth surface using a `CylinderGeometry` with a hemispherical copper dome cap

2. **Magnifying transmitter toroidal field**:
   - Generate the toroidal magnetic field as a `TorusGeometry` (majorRadius = tower height × 2, tubularSegments 128) centered at the tower top
   - Animate the torus with a `ShaderMaterial` that propagates a traveling wave phase along the tube: `colorIntensity = 0.5 + 0.5·sin(uTubeAngle − time·uFrequency)`
   - Add a second, counter-rotating torus at 90° to produce the characteristic Tesla magnifying transmitter field orthogonality

3. **Longitudinal standing wave nodes**:
   - Compute Earth-resonance cavity node positions: for mode `n`, nodes appear at `latitude = ±arccos(cos(n·π/N_nodes))`
   - Render each node as a glowing `RingGeometry` (horizontal disc) on the Earth surface using an emissive, pulsing `ShaderMaterial`
   - Animate antinode rings expanding and contracting in phase with `sin(time·resonantFrequency)`

4. **Ground-return current sheet**:
   - Simulate radial ground return currents as 20 000 GPU particles emanating from the antipodal point and sweeping back toward the tower along the Earth's surface
   - Each particle traces a great-circle arc on the sphere surface; compute the arc position in the TSL vertex shader using `slerp(startDir, endDir, fract(time·speed + offset))`
   - Color particles by current density (red near source/antipode, fading to blue mid-arc)

5. **Radial electric field pulses**:
   - Emit radial pulse rings from the tower base outward along the Earth surface every `1/frequency` seconds
   - Each ring is a `RingGeometry` scaled outward over time via a `scale` uniform; fade opacity as the ring expands
   - At the antipodal point, rings reconverge and produce a constructive interference burst (extra `Bloom` flash via a point light pulse)

6. **Post-processing**:
   - `Bloom` (threshold 0.2, intensity 1.8) for the field nodes and pulse rings
   - `GodRays` from the Wardenclyffe tower dome
   - `Scanlines` (subtle) to evoke a historical oscilloscope aesthetic

7. **Runtime controls (lil-gui)**:
   - `resonant_frequency` (1–100 Hz) — primary resonance frequency driving all animations
   - `wave_mode` (1–12) — selects the Earth-cavity resonance mode, changing node count
   - `transmission_power` (0–1) — scales field intensity and particle count
   - `ground_current_density` (5k–100k particles)
   - Toggles: `show_toroidal_field`, `show_standing_nodes`, `show_ground_currents`, `show_ionosphere`

## Output Format

```
TeslaStandingWaveScene/
├── TeslaStandingWaveScene.jsx
├── components/
│   ├── EarthGlobe.jsx           ← Earth + ionosphere spheres
│   ├── WardenclyffeTower.jsx    ← Tower geometry + dome
│   ├── ToroidalField.jsx        ← Animated torus field ShaderMaterial
│   ├── StandingNodes.jsx        ← RingGeometry resonance node rings
│   ├── GroundCurrents.jsx       ← Points + TSL great-circle arc shader
│   ├── PulseRings.jsx           ← Expanding ring emissions
│   └── PostFX.jsx
├── shaders/
│   ├── greatCircleArc.tsl.js   ← TSL slerp great-circle particle path
│   └── toroidalWave.tsl.js     ← Traveling wave phase shader
└── controls/gui.js
```

## Boundaries

- Do NOT conflate Tesla's longitudinal wave model with transverse electromagnetic waves — the visualization must show radial/longitudinal propagation through the Earth volume, not away from a dipole antenna.
- Do NOT model Tesla's claims as experimentally verified long-range wireless power transmission; present them as historically documented experiments and engineering patents.
- Do NOT recreate geometry per frame — reuse all `BufferGeometry` attributes.
- Always feature-detect WebGPU before using compute for ground-current particle integration.
