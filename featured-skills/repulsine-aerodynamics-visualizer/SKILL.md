---
name: repulsine-aerodynamics-visualizer
description: Masterfully designs a real-time 3D aerodynamics visualization of Viktor Schauberger's Repulsine — a vortex implosion disc with spiraling dual-vortex airflow, centripetal fluid dynamics, and toroidal pressure differentials. Invoke when asked to build, render, or animate a Repulsine, vortex disc, implosion engine, or Schauberger fluid device in 3D.
---

# Repulsine Aerodynamics Visualizer

Produces a masterful, physically-informed real-time 3D visualization of the Repulsine — Viktor Schauberger's vortex implosion disc — using Three.js r182+ (WebGL renderer), React Three Fiber v9, custom TSL/GLSL shaders, and GPU-accelerated particle systems. The visualization communicates the device's dual counter-rotating vortex structure, centripetal implosion dynamics, wave-disc geometry, and toroidal pressure field with interactive runtime controls.

## When to Use

- User asks to visualize, animate, or render the Repulsine or any Schauberger vortex implosion device
- User wants to demonstrate dual counter-rotating vortex aerodynamics in 3D
- A real-time, interactive WebGL/WebGPU fluid dynamics or aerodynamics demo is needed
- User is building an educational or research tool around implosion physics or fringe aerodynamics
- User asks for a Three.js scene featuring logarithmic spiral particle flows, pressure field heatmaps, or wave-disc geometry

## Stack

| Layer | Library | Version |
|---|---|---|
| 3D Renderer | Three.js `WebGLRenderer` | r182+ |
| React Integration | React Three Fiber | v9 (React 19) |
| Helpers | `@react-three/drei` | latest |
| Particle System | Three.js `Points` + `BufferGeometry` | native |
| Post-Processing | `@react-three/postprocessing` | latest |
| Physics/Compute | Three.js TSL + WebGPU compute | r182+ |
| UI Controls | lil-gui | latest |
| Math | `gl-matrix` | v3 |

## Process

1. **Scene setup and renderer configuration**:
   - Initialize `WebGLRenderer` with `antialias: true`, `powerPreference: 'high-performance'`
   - Set `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` to cap Retina overhead
   - Feature-detect WebGPU and, if available, bind a compute pipeline for particle physics; keep `WebGLRenderer` for the visible scene
   - Wrap in an R3F `<Canvas>` with `gl={{ antialias: true }}` and `frameloop="always"`

2. **Repulsine disc geometry**:
   - Model upper and lower disc housings as `LatheGeometry` (profile revolution) for the characteristic lens shape
   - Use `InstancedMesh` to render the thousands of hyperbolic wave channels machined into the disc — each channel is a sinusoidal trough; animate rotation via a `time` uniform in the vertex shader
   - Apply `MeshTransmissionMaterial` (Drei) to the glass dome for the refractive, iridescent effect
   - Model the central implosion cone as an inverted `ConeGeometry` with a spiraling `ShaderMaterial`

3. **Dual vortex streamlines**:
   - Outer centrifugal spiral: generate a logarithmic spiral tube — `r = a·e^(b·θ)` — as a `TubeGeometry` wrapping outward from the disc rim; animate via a `time`-driven offset uniform
   - Inner centripetal implosion cone: a tightening inward spiral tube that converges at the central axis, counter-rotating relative to the outer
   - Update `BufferGeometry.attributes.position.needsUpdate = true` each frame on reusable buffers — never recreate geometry per frame
   - Encode velocity magnitude as color (blue = slow → red = fast) via a `DataTexture` LUT sampled in the `ShaderMaterial`

4. **GPU particle aerodynamic flow**:
   - Spawn 50 000–200 000 particles using Three.js `Points` with a custom TSL/GLSL vertex shader
   - Each particle's position is computed deterministically from `time + instanceOffset` — no CPU physics loop
   - Bake the vortex velocity field into a `DataTexture` (RGBA32F); sample it in the vertex shader to modulate particle speed and radial displacement
   - When WebGPU compute is available, run a TSL `Fn()` compute kernel to integrate trajectories on GPU for a 10× throughput gain

5. **Pressure field heatmap**:
   - Bake a 2D Bernoulli-inspired pressure gradient (low at center, high at rim) into a `DataTexture`
   - Render as a transparent plane parallel to the disc using a `ShaderMaterial` that blends pressure color (purple = low, yellow = high) additively
   - Animate the texture each frame by writing a new `Float32Array` or use render-target ping-pong for GPU-side evolution

6. **Post-processing**:
   - `Bloom` (threshold 0.6, radius 0.8, intensity 1.4) to illuminate the vortex energy cores
   - `ChromaticAberration` (offset 0.002) for the prismatic glass housing
   - Optional `GodRays` emanating from the central implosion axis

7. **TSL shader authoring**:
   - Write all custom shaders in TSL (`three/tsl`) so they compile to both GLSL and WGSL without duplication
   - Model the spiral trajectory as composable TSL nodes: `spiralR = float(a).mul(exp(float(b).mul(theta)))`
   - Use `Fn()` to define reusable functions for pressure lookup, velocity coloring, and implosion displacement

8. **Runtime controls (lil-gui)**:
   - `vortex_rpm` (50–5000) — outer disc rotation speed
   - `implosion_strength` (0–1) — centripetal inward pull on particle trajectories
   - `particle_count` (10k–200k) — particle density
   - `pressure_scale` (0.1–5) — heatmap gradient intensity
   - `fluid_viscosity` (0.01–1) — spiral tightness coefficient `b`
   - Toggles: `show_streamlines`, `show_particles`, `show_pressure_field`, `show_housing`

9. **Performance optimizations**:
   - `InstancedMesh` for wave-disc channels → single draw call for thousands of surface features
   - `THREE.LOD` — high-res vortex tubes near camera, simplified lines at distance ≥ 50 units
   - `content-visibility: auto` on the wrapper `<div>` to suspend rendering off-screen

## Output Format

Produce a self-contained React component tree:

```
RepulsineScene/
├── RepulsineScene.jsx        ← Root R3F Canvas component
├── components/
│   ├── DiscGeometry.jsx      ← Wave-disc InstancedMesh + glass housing
│   ├── VortexStreamlines.jsx ← Dual spiral TubeGeometry + ShaderMaterial
│   ├── ParticleFlow.jsx      ← Points + TSL/GLSL vertex shader
│   ├── PressureField.jsx     ← DataTexture heatmap plane
│   └── PostFX.jsx            ← Bloom, ChromaticAberration, GodRays
├── shaders/
│   ├── spiral.tsl.js         ← TSL spiral trajectory node functions
│   └── pressureLUT.js        ← DataTexture pressure gradient builder
└── controls/
    └── gui.js                ← lil-gui parameter bindings
```

The scene renders interactively at 60 fps on a mid-range GPU with 100k particles.

## Examples

### Example Input
```
Build a real-time 3D Repulsine visualization with animated vortex particle flow, a pressure
heatmap, and runtime controls for RPM, particle count, and implosion strength.
```

### Example Output
```jsx
// RepulsineScene.jsx
import { Canvas } from '@react-three/fiber'
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing'
import { DiscGeometry } from './components/DiscGeometry'
import { VortexStreamlines } from './components/VortexStreamlines'
import { ParticleFlow } from './components/ParticleFlow'
import { PressureField } from './components/PressureField'
import { useGUI } from './controls/gui'

export function RepulsineScene() {
  const params = useGUI()
  return (
    <Canvas gl={{ antialias: true, powerPreference: 'high-performance' }}
            camera={{ position: [0, 3, 6], fov: 55 }}>
      <ambientLight intensity={0.2} />
      <DiscGeometry rpm={params.vortex_rpm} />
      <VortexStreamlines strength={params.implosion_strength} visible={params.show_streamlines} />
      <ParticleFlow count={params.particle_count} viscosity={params.fluid_viscosity} />
      <PressureField scale={params.pressure_scale} visible={params.show_pressure_field} />
      <EffectComposer>
        <Bloom luminanceThreshold={0.6} radius={0.8} intensity={1.4} />
        <ChromaticAberration offset={[0.002, 0.002]} />
      </EffectComposer>
    </Canvas>
  )
}
```

## Boundaries

- Do NOT use Babylon.js, A-Frame, or Plotly — they lack the fine-grained shader access required.
- Do NOT use `WebGPURenderer` as the primary renderer — it carries a 2–4× penalty over `WebGLRenderer` for multi-mesh scenes; use WebGPU only for the compute layer.
- Do NOT recreate `BufferGeometry` or allocate new `Float32Array` objects in the render loop — reuse and set `needsUpdate = true`.
- Do NOT use raw GLSL string templates when TSL is available — TSL compiles to both GLSL and WGSL and surfaces bugs earlier.
- Do NOT add more than 5 dynamic shadow-casting lights; bake static lighting instead.
- Always cap `renderer.setPixelRatio` at 2 to avoid 4× fragment shading on high-DPI displays.
- Always feature-detect WebGPU before using compute shaders; fall back gracefully to CPU-side updates.
