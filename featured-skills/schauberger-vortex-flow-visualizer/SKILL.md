---
name: schauberger-vortex-flow-visualizer
description: Designs a real-time 3D visualization of Viktor Schauberger's implosion water-vortex dynamics — hyperbolic spiral flow, inward centripetal suction, temperature-stratified laminar streams, and the trout-curve velocity profile. Invoke when asked to visualize Schauberger's living water, implosion vortex, egg-shaped vessel, or nature-based fluid motion in 3D.
---

# Schauberger Vortex Flow Visualizer

Produces a real-time 3D visualization of Viktor Schauberger's implosion water-vortex system — the "living water" motion that spirals inward along a hyperbolic path, cools as it implodes, and generates the suction force Schauberger observed in mountain streams and engineered into his egg-shaped vessels. Built on Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particles.

## When to Use

- User asks to visualize Schauberger's vortex, living water, implosion flow, or nature-aligned fluid dynamics
- User wants to render an egg-shaped implosion vessel with animated interior flow
- A 3D demonstration of centripetal vs. centrifugal fluid motion is needed
- User is building an educational tool around biomimetic or nature-inspired engineering
- User wants to show temperature-stratified flow or the trout-curve velocity profile in 3D

## Process

1. **Egg-vessel geometry**:
   - Construct the characteristic Schauberger egg shape using a `LatheGeometry` built from a parametric profile curve (wider at the base, narrowing to a point at the top) — this is the vessel cross-section revolved 360°
   - Render the shell with `MeshTransmissionMaterial` (Drei): `transmission: 0.85`, `roughness: 0.02`, `thickness: 0.4`, tinted blue-green to suggest water glass
   - Add a subtle `WireframeGeometry` overlay at low opacity to reveal the vessel's hyperbolic curvature

2. **Spiral vortex particle flow**:
   - Generate 80 000 particles tracing the hyperbolic inward spiral path inside the vessel
   - Each particle follows: `r(t) = r₀ · e^(−k·t)`, `θ(t) = ω·t`, `z(t) = z₀ − v_z·t` — a 3D logarithmic implosion spiral computed entirely in the TSL vertex shader
   - Color particles by temperature (deep blue = cold center, warm green-gold = outer warmer layer) using a `DataTexture` temperature LUT
   - Vary `k`, `ω`, `v_z` per particle via `Float32Array` attributes to produce the characteristic laminar-to-coherent flow structure

3. **Trout-curve velocity profile**:
   - Render a cross-section velocity field as a 2D `DataTexture` heat overlay on a clipping plane through the vessel midpoint
   - Use a `ShaderMaterial` that maps local flow speed to color: fast core (white), mid-band (cyan), slow outer wall (deep blue) — mimicking the parabolic-to-hyperbolic velocity profile Schauberger measured in trout streams

4. **Temperature stratification layers**:
   - Render concentric `RingGeometry` cross-sections inside the vessel at five temperature isotherms
   - Each ring's `ShaderMaterial` uses a `sin(time + phaseOffset)` undulation to simulate the pulsing thermal stratification in vortex flow
   - Color from 4 °C (maximum-density, deepest blue) outward to ambient temperature (warm green)

5. **Implosion suction effect**:
   - At the vessel apex (top narrowing point) render a converging `ConeGeometry` with a pulsing emissive `ShaderMaterial` to represent the implosion suction node
   - Add a `PointLight` at the apex (color `#aaddff`, intensity `0.5 + 0.3·sin(time·3)`) to illuminate the convergence zone
   - Trail 5 000 fast-moving "suction filament" particles that accelerate exponentially toward the apex

6. **Post-processing**:
   - `Bloom` (threshold 0.4, intensity 1.2) for the cold luminous vortex core
   - `DepthOfField` (focusDistance 0.5, focalLength 0.02, bokehScale 3) to focus on the vessel interior
   - Subtle `Vignette` to frame the vessel

7. **Runtime controls (lil-gui)**:
   - `flow_rate` (0.1–5) — scales `v_z`, the axial advection speed
   - `spiral_tightness` (0.01–0.5) — controls `k`, the radial implosion coefficient
   - `rotation_speed` (0.1–10 rad/s) — angular velocity `ω` of the vortex
   - `temperature_gradient` (0–1) — intensity of the thermal color stratification
   - `particle_count` (10k–200k) — flow particle density
   - Toggles: `show_velocity_field`, `show_isotherms`, `show_suction_node`, `show_vessel_shell`

## Output Format

```
SchaubergerScene/
├── SchaubergerScene.jsx
├── components/
│   ├── EggVessel.jsx           ← LatheGeometry transmission shell
│   ├── SpiralParticleFlow.jsx  ← Points + TSL implosion spiral shader
│   ├── VelocityField.jsx       ← DataTexture cross-section heatmap
│   ├── ThermalIsotherms.jsx    ← RingGeometry temperature bands
│   ├── ImplosionApex.jsx       ← Converging cone + suction filaments
│   └── PostFX.jsx
├── shaders/
│   ├── implosionSpiral.tsl.js  ← TSL logarithmic implosion spiral
│   └── temperatureLUT.js       ← DataTexture 4°C→ambient color map
└── controls/gui.js
```

## Boundaries

- Do NOT model the vortex as centrifugal (outward) — Schauberger's key insight is centripetal (inward) implosion; always spiral inward toward the axis and apex.
- Do NOT allocate new geometry per frame — update `BufferGeometry` attribute arrays in place.
- Do NOT use `WebGPURenderer` as the primary renderer — use it only for the optional particle compute layer.
- Always present Schauberger's theoretical claims as historically documented observations and engineering experiments, not peer-reviewed fluid dynamics.
