---
name: russell-cosmogony-visualizer
description: Designs a real-time 3D visualization of Walter Russell's wave cosmogony — the dual opposed vortex compression/expansion model of atomic formation, the cube-sphere pressure geometry, centripetal/centrifugal wave cycles, and Russell's nine-octave periodic table wave structure. Invoke when asked to visualize Walter Russell's cosmogony, Russell's atomic model, wave-vortex matter creation, or Russell's periodic table in 3D.
---

# Walter Russell Cosmogony Visualizer

Produces a real-time 3D visualization of Walter Russell's cosmogony — the wave universe in which all matter is formed by dual opposed vortex cones compressing toward a cathode seed point and expanding outward from an anode fulcrum, governed by the cube-sphere pressure geometry and the nine-octave wave structure of the periodic table — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particles.

## When to Use

- User asks to visualize Walter Russell's cosmogony, wave universe, or atomic wave-vortex model
- User wants a 3D rendering of Russell's dual-opposed vortex cone matter-formation process
- An interactive demonstration of Russell's cube-sphere wave pressure geometry is needed
- User is building an educational or philosophical tool around Russell's unified field theory or periodic table interpretation
- User wants to render centripetal/centrifugal wave cycles or Russell's nine-octave wave series in 3D

## Process

1. **Dual opposed vortex cone geometry**:
   - Model Russell's two opposed vortex cones as `ConeGeometry` objects pointing toward each other along the Y-axis — the upper cone points downward (centripetal compression toward cathode seed), the lower cone points upward (centrifugal expansion toward anode fulcrum)
   - Animate both cones rotating in opposite directions: the compressing (upper) cone clockwise, the expanding (lower) cone counter-clockwise
   - Apply a `ShaderMaterial` that maps vertex height to color: dark void-black at the cone apex (cathode seed), brightening through red-orange toward the wide base (anode)
   - Emit spiral particle streams along the cone surface inward toward the seed point (compression cone) and outward from it (expansion cone)

2. **Cathode seed point and anode fulcrum**:
   - At the midpoint between the two cones, render the cathode seed as a small, intensely glowing `SphereGeometry` — this is Russell's "point of rest" where matter condenses
   - Render the anode fulcrum as a flat `RingGeometry` disc orthogonal to the cone axis — the equatorial "wave amplitude plane"
   - Animate the seed sphere pulsing with `scale = 1 + 0.3·sin(time·octave_frequency)` to simulate the rhythmic heartbeat of Russell's wave compression

3. **Cube-sphere pressure geometry**:
   - Render the bounding pressure cube as a `BoxGeometry` wireframe oriented 45° (rotated so its diagonal aligns with the cone axis) — Russell's cube is the "static" pressure equilibrium
   - Inside the cube, inscribe a `SphereGeometry` representing the dynamic pressure sphere — animate it oscillating between a perfect sphere (maximum compression) and a slightly prolate spheroid (maximum expansion) via vertex shader displacement
   - Alternate the cube wireframe color between cold blue (compression half-cycle) and warm amber (expansion half-cycle)

4. **Nine-octave wave series**:
   - Arrange nine concentric `TorusGeometry` rings around the seed point at logarithmically increasing radii — representing Russell's nine octaves of atomic formation
   - Color each octave ring by its position in the Russell periodic table analogy: hydrogen (innermost, violet-white) through carbon, silicon, and out to radium (outermost, deep red)
   - Animate each ring oscillating vertically with `y = A_n·sin(2π·f_n·time)` where `f_n = f₀·2^n` — each octave at double the frequency of the previous

5. **Centripetal/centrifugal wave cycle particles**:
   - Spawn two distinct particle populations: 40 000 "centripetal" particles converging inward along spiral paths toward the seed point, and 40 000 "centrifugal" particles spiraling outward from it
   - Centripetal particles accelerate as they approach the seed (velocity ∝ `1/r²`); centrifugal particles decelerate as they recede
   - Both populations computed in the TSL vertex shader from `time + phaseOffset` with no CPU physics loop

6. **Light/dark cycle overlay**:
   - Render Russell's "light/dark" half-cycle as a subtle animated `PlaneGeometry` overlay bisecting the scene: left half lit (expansion/light), right half dark (compression/dark)
   - Animate the dividing plane oscillating sinusoidally across the scene to show the rhythmic interchange

7. **Post-processing**:
   - `Bloom` (threshold 0.2, intensity 2.0) for the seed point and octave rings
   - `DepthOfField` focused on the cathode seed
   - Gentle `Vignette` to frame the cosmological void

8. **Runtime controls (lil-gui)**:
   - `octave_frequency` (0.1–5 Hz) — base wave cycle frequency, doubling per octave
   - `compression_strength` (0–1) — strength of centripetal inward pull
   - `active_octave` (1–9) — highlights the selected octave ring and its element analog
   - `particle_density` (10k–100k per stream)
   - Toggles: `show_cube_geometry`, `show_octave_rings`, `show_particles`, `show_light_dark_cycle`

## Output Format

```
RussellCosmogonyScene/
├── RussellCosmogonyScene.jsx
├── components/
│   ├── DualVortexCones.jsx      ← Opposed ConeGeometry + ShaderMaterial
│   ├── CathodeSeed.jsx          ← Glowing pulsing SphereGeometry
│   ├── CubeSphereGeometry.jsx   ← Wireframe cube + deforming sphere
│   ├── OctaveRings.jsx          ← Nine concentric TorusGeometry rings
│   ├── WaveParticles.jsx        ← Centripetal + centrifugal Points streams
│   ├── LightDarkCycle.jsx       ← Bisecting plane overlay
│   └── PostFX.jsx
├── shaders/
│   ├── vortexCone.tsl.js       ← TSL cone spiral stream shader
│   └── octaveRing.tsl.js       ← TSL oscillating octave ring shader
└── controls/gui.js
```

## Boundaries

- Do NOT present Russell's cosmogony as accepted physics — it is a philosophical and artistic model of the universe; label it clearly as Russell's speculative framework.
- Do NOT conflate Russell's nine-octave table with the standard IUPAC periodic table; present it as Russell's alternative conceptual organization.
- Do NOT recreate geometry per frame — reuse all `BufferGeometry` attributes.
- Present Russell's model in its early 20th-century philosophical context as a visionary synthesis of art, science, and metaphysics.
