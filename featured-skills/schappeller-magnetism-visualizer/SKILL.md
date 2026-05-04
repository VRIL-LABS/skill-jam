---
name: schappeller-magnetism-visualizer
description: Masterfully designs a real-time 3D visualization of Karl Schappeller's glowing magnetism device — a spherical prime mover driven by glowing etheric plasma, radiant magnetic field lines, and a luminiferous aether vortex core. Invoke when asked to visualize Schappeller's sphere, glowing magnetism, etheric plasma, or aether-field energy devices in 3D.
---

# Schappeller Glowing Magnetism Visualizer

Produces a masterful real-time 3D visualization of Karl Schappeller's "glowing magnetism" prime mover — a hollow sphere energized by a radiant etheric plasma core, surrounded by self-organizing magnetic field lines, glowing filamentary discharge patterns, and a luminous aether vortex — using Three.js r182+ (WebGL renderer), React Three Fiber v9, TSL/GLSL volumetric shaders, and GPU particle systems. The visualization captures both the outer magnetostatic field geometry and the inner luminous plasma dynamics.

## When to Use

- User asks to visualize, animate, or render Karl Schappeller's sphere or glowing magnetism device
- User wants a 3D representation of etheric plasma, self-luminous magnetic field lines, or radiant aether fields
- An interactive WebGL visualization of unconventional electromagnetic or aether-field phenomena is needed
- User is building an educational or speculative-physics tool around Schappeller's prime mover, the "Ether" concept, or zero-point field devices
- User needs volumetric glow, magnetic field line geometry, or plasma filament rendering in Three.js

## Stack

| Layer | Library | Version |
|---|---|---|
| 3D Renderer | Three.js `WebGLRenderer` | r182+ |
| React Integration | React Three Fiber | v9 (React 19) |
| Helpers | `@react-three/drei` | latest |
| Volumetric Glow | Custom `ShaderMaterial` + `RawShaderMaterial` | native |
| Post-Processing | `@react-three/postprocessing` | latest |
| Particle System | Three.js `Points` + `BufferGeometry` | native |
| Physics/Compute | Three.js TSL + optional WebGPU compute | r182+ |
| UI Controls | lil-gui | latest |

## Process

1. **Scene and renderer setup**:
   - Initialize `WebGLRenderer` with `antialias: true`, `logarithmicDepthBuffer: true` for the sphere interior depth precision
   - Enable alpha on the renderer for the transparent outer shell
   - Set `toneMapping: THREE.ACESFilmicToneMapping` and `toneMappingExposure: 1.8` to render the glowing plasma correctly

2. **Schappeller sphere geometry**:
   - Outer shell: `SphereGeometry` (radius 1, segments 64) with `MeshTransmissionMaterial` (Drei) — `transmission: 0.9`, `roughness: 0.05`, `ior: 1.5` — to simulate the glowing glass/ceramic casing
   - Inner plasma core: a smaller inverted `SphereGeometry` rendered with a volumetric `ShaderMaterial` that raymarches a density field inside the sphere; the density function produces a glowing, pulsing oval of luminous plasma
   - Polar rod electrodes: two thin `CylinderGeometry` objects along the Y-axis, rendered with an emissive `MeshStandardMaterial` (emissiveIntensity driven by a `sin(time)` uniform)

3. **Magnetic field line geometry**:
   - Generate closed magnetic dipole field lines analytically: for a dipole at the origin, the field line passing through colatitude θ₀ follows `r = r₀·sin²(θ)` in spherical coordinates
   - Tesselate each field line into a `TubeGeometry` (radialSegments 4, tubular segments 128)
   - Render with a `ShaderMaterial` that colors lines by field strength: `B ∝ 1/r³`, mapped via a warm-to-cool `DataTexture` LUT (gold near poles → cyan at equator)
   - Animate a traveling pulse along each field line by offsetting a `uv.x` lookup into the LUT with `time`

4. **Glowing plasma filaments**:
   - Spawn 30 000 particles (Three.js `Points`) constrained inside the sphere volume
   - Each filament particle follows a helical path spiraling between the poles: `x = r·cos(ω·t + φ)`, `y = v_z·t mod height`, `z = r·sin(ω·t + φ)`, computed entirely in the TSL/GLSL vertex shader
   - Color each particle by its proximity to the polar axis — deeper blue-white near the axis, amber-gold at the periphery
   - Vary `r` and `ω` per particle using a `Float32Array` attribute encoding individual phase and amplitude offsets

5. **Volumetric etheric aether glow**:
   - Place a `PointLight` at the sphere center with color `#ffeedd` and intensity driven by `0.8 + 0.2·sin(time·2.5)` to simulate the pulsing "glowing" discharge
   - Add a screen-space volumetric glow pass using `@react-three/postprocessing` `GodRays` with the inner plasma sphere as the light source mesh
   - Apply `Bloom` (threshold 0.3, intensity 2.5) to capture the characteristic soft, diffuse luminosity of Schappeller's "primary light"

6. **Aether vortex core**:
   - At the sphere's center render a `TorusKnotGeometry` (p=2, q=3) scaled to 0.15 as the "prime mover" knot; apply a fully emissive `MeshStandardMaterial` cycling through `hsl(time*20, 100%, 70%)` via a TSL `colorNode`
   - Surround it with a tight particle vortex (5 000 particles) spiraling inward along the Z-axis using a TSL compute shader when WebGPU is available

7. **Runtime controls (lil-gui)**:
   - `plasma_intensity` (0–3) — scales the inner plasma density and emissive brightness
   - `field_line_count` (6–48) — number of dipole field lines rendered
   - `pulse_frequency` (0.5–10 Hz) — frequency of the polar electrode discharge pulse
   - `particle_density` (5k–100k) — plasma filament particle count
   - `field_strength` (0.1–5) — scales the dipole field line radius/spread
   - Toggles: `show_field_lines`, `show_plasma`, `show_outer_shell`, `show_vortex_core`

8. **Performance optimizations**:
   - All field-line tubes share a single `ShaderMaterial` instance — only uniforms vary
   - Plasma particles use attribute-driven GPU animation — zero CPU physics per frame
   - The inner volume raymarcher uses a bounded sphere ray-AABB test to skip fragments outside the plasma volume early

## Output Format

Produce a self-contained React component tree:

```
SchappellerScene/
├── SchappellerScene.jsx       ← Root R3F Canvas component
├── components/
│   ├── OuterSphere.jsx        ← Transmission glass shell + electrodes
│   ├── PlasmaCore.jsx         ← Volumetric raymarched glow sphere
│   ├── FieldLines.jsx         ← Dipole TubeGeometry + animated LUT shader
│   ├── PlasmaFilaments.jsx    ← Points + TSL helical vertex shader
│   ├── AetherVortex.jsx       ← TorusKnot emissive + tight spiral particles
│   └── PostFX.jsx             ← Bloom, GodRays
├── shaders/
│   ├── plasmaVolume.tsl.js    ← Raymarched density field in TSL
│   ├── fieldLineLUT.js        ← DataTexture field strength color map
│   └── helicalParticle.tsl.js ← TSL helical trajectory functions
└── controls/
    └── gui.js                 ← lil-gui parameter bindings
```

## Examples

### Example Input
```
Create an interactive 3D visualization of Karl Schappeller's glowing magnetism sphere
showing the magnetic field lines, inner plasma glow, and the pulsing aether vortex core.
```

### Example Output
```jsx
// SchappellerScene.jsx
import { Canvas } from '@react-three/fiber'
import { EffectComposer, Bloom, GodRays } from '@react-three/postprocessing'
import { OuterSphere } from './components/OuterSphere'
import { PlasmaCore } from './components/PlasmaCore'
import { FieldLines } from './components/FieldLines'
import { PlasmaFilaments } from './components/PlasmaFilaments'
import { AetherVortex } from './components/AetherVortex'
import { useGUI } from './controls/gui'
import { useRef } from 'react'

export function SchappellerScene() {
  const params = useGUI()
  const plasmaRef = useRef()
  return (
    <Canvas gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}
            camera={{ position: [0, 0, 4], fov: 50 }}>
      <OuterSphere visible={params.show_outer_shell} />
      <PlasmaCore ref={plasmaRef} intensity={params.plasma_intensity} visible={params.show_plasma} />
      <FieldLines count={params.field_line_count} strength={params.field_strength}
                  visible={params.show_field_lines} />
      <PlasmaFilaments count={params.particle_density} frequency={params.pulse_frequency} />
      <AetherVortex visible={params.show_vortex_core} />
      <EffectComposer>
        <Bloom luminanceThreshold={0.3} intensity={2.5} />
        <GodRays sun={plasmaRef} density={0.96} decay={0.93} weight={0.3} />
      </EffectComposer>
    </Canvas>
  )
}
```

## Boundaries

- Do NOT model Schappeller's device as a conventional electromagnet — it must be rendered as a self-luminous etheric plasma phenomenon with field geometry distinct from a standard dipole.
- Do NOT use raw GLSL string templates when TSL is available — write shaders in TSL for portability.
- Do NOT recreate geometry or allocate typed arrays inside the render loop — reuse `BufferGeometry` attributes.
- Do NOT use more than 3 dynamic shadow-casting lights — bake the sphere's ambient contribution into a `CubeCamera` environment map instead.
- Always cap `renderer.setPixelRatio` at 2.
- Qualify any physical or scientific claims about Schappeller's theory as speculative and historically contextual, not empirically verified physics.
