---
name: leedskalnin-magnetic-current-visualizer
description: Designs a real-time 3D visualization of Ed Leedskalnin's dual magnetic current theory — two counter-streaming screws of individual North and South magnetic monopole flows, their helical paths through matter, and the coral castle levitation hypothesis. Invoke when asked to visualize Leedskalnin's magnetic current, individual magnets, dual magnetic screws, or the Coral Castle levitation theory in 3D.
---

# Leedskalnin Dual Magnetic Current Visualizer

Produces a real-time 3D visualization of Ed Leedskalnin's unconventional magnetic theory — two streams of individual North-pole and South-pole "magnets" flowing in opposite helical screws through conductors and the Earth, interacting with matter to produce Leedskalnin's alleged levitation and quarrying techniques at Coral Castle — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particles.

## When to Use

- User asks to visualize Leedskalnin's magnetic current, individual north/south magnets, or dual magnetic screws
- User wants a 3D rendering of counter-streaming helical magnetic particle flows through a conductor
- An interactive demonstration of Leedskalnin's alternative magnetic model is needed
- User is building an educational tool around Coral Castle, Ed Leedskalnin's experiments, or alternative electromagnetism
- User wants to render two-fluid magnetic current flows, helical screw paths, or magnetic current generator animations

## Process

1. **Conductor and coil geometry**:
   - Model a simple horseshoe magnet as two `BoxGeometry` legs with a `CylinderGeometry` arc, colored red (North) and blue (South) per pole
   - Model a coil of wire as a helical `TubeGeometry` generated from a parametric helix path: `x = R·cos(θ)`, `y = p·θ`, `z = R·sin(θ)` with `n` turns
   - Add a straight conductor bar `CylinderGeometry` for the basic current-flow demonstration
   - Render all conductor metal with `MeshStandardMaterial({ metalness: 0.9, roughness: 0.2, color: 0xb87333 })` (copper)

2. **Dual magnetic current streams — North screw**:
   - Spawn 30 000 "North individual magnet" particles (shown as small red spheres via `Points` with a circular point texture) flowing through the conductor in one helical direction
   - Each particle traces a right-handed helical path: `x(t) = R·cos(ω·t + φ)`, `y(t) = v·t mod L`, `z(t) = R·sin(ω·t + φ)`, computed in the TSL vertex shader
   - Particles glow bright red-orange; use `Bloom` to amplify the "individual magnet" luminosity
   - When particles exit the conductor end, curl outward into the external field path and return to the entry end

3. **Dual magnetic current streams — South screw**:
   - Spawn 30 000 "South individual magnet" particles flowing in the opposite helical direction (left-handed screw, `ω` negated)
   - Render as small blue-cyan `Points` on a counter-rotating helix — exact mirror of the North stream
   - The two streams visually interpenetrate and pass through each other, as per Leedskalnin's claim that they flow simultaneously through the same conductor

4. **External field loop visualization**:
   - Show the complete circuit of each magnetic stream as looping paths outside the conductor: North particles arch from North pole through space to South pole; South particles loop the reverse
   - Render these external paths as semi-transparent `TubeGeometry` arcs using a `ShaderMaterial` that fades opacity with distance from the conductor
   - Animate a traveling brightness pulse along each tube at the stream's flow velocity

5. **Coral Castle levitation hypothesis**:
   - Show a stylized coral limestone block (`BoxGeometry` with a coral-texture `MeshStandardMaterial`) suspended above the horseshoe magnet
   - Animate the block rotating slowly as Leedskalnin claimed to spin blocks to neutralize gravity
   - Render the "neutralizing" magnetic current streams as a symmetrical crossing pattern of North and South particles meeting at the block's center — the equal-opposite flows cancel the "gravity pull" in Leedskalnin's model
   - Label this section clearly as "Leedskalnin's Theoretical Model — Unverified"

6. **Magnetic current generator animation**:
   - Model Leedskalnin's PMH (Permanent Magnet Holder) as a U-shaped iron core with two bar magnets bridged across it
   - Animate the dual magnetic current streams circulating continuously through the closed iron loop
   - Show the current switching direction when the bridge magnet is flipped (a toggle control)

7. **Post-processing**:
   - `Bloom` (threshold 0.2, intensity 2.0) for the particle streams and external field arcs
   - `ChromaticAberration` (offset 0.001) for the conductor material
   - Subtle `Vignette` to focus on the central device

8. **Runtime controls (lil-gui)**:
   - `flow_speed` (0.1–5) — velocity of both magnetic current streams
   - `stream_density` (5k–100k per polarity) — particle count per stream
   - `coil_turns` (1–20) — number of turns in the coil geometry
   - `levitation_mode` (toggle) — activates the Coral Castle block levitation animation
   - `pmh_mode` (toggle) — switches from horseshoe magnet to PMH closed-loop display
   - Toggles: `show_north_stream`, `show_south_stream`, `show_external_field`, `show_levitation_hypothesis`

## Output Format

```
LeedskalnInScene/
├── LeedskalnInScene.jsx
├── components/
│   ├── MagnetCoilGeometry.jsx    ← Horseshoe magnet + helical coil + bar
│   ├── NorthCurrentStream.jsx    ← Right-handed helix Points + TSL shader
│   ├── SouthCurrentStream.jsx    ← Left-handed helix Points + TSL shader
│   ├── ExternalFieldArcs.jsx     ← TubeGeometry external loop paths
│   ├── CoralCastleBlock.jsx      ← Levitating block + "neutralizing" stream
│   ├── PMHGenerator.jsx          ← U-core PMH closed-loop animation
│   └── PostFX.jsx
├── shaders/
│   ├── magneticScrew.tsl.js     ← TSL helical screw path shader
│   └── fieldArcFade.tsl.js      ← TSL distance-faded arc tube shader
└── controls/gui.js
```

## Boundaries

- Do NOT present Leedskalnin's "individual magnet" model as established physics — it contradicts the dipole nature of magnetic fields as established by Maxwell's equations; label it as Leedskalnin's personal alternative theory.
- Do NOT suggest the visualization provides engineering instructions for levitation.
- Do NOT recreate geometry per frame — reuse all `BufferGeometry` attributes.
- Always distinguish clearly between the verifiable behavior of magnets and Leedskalnin's alternative interpretive model.
- Present Leedskalnin's work in its historical context as an autodidact's experiments documented in self-published booklets in the 1940s.
