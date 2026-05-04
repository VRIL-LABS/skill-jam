---
name: rife-resonance-visualizer
description: Designs a real-time 3D visualization of Royal Raymond Rife's plasma tube resonance system — mortal oscillatory rate (MOR) frequency fields, plasma tube emission spectra, standing wave resonance chambers, and cellular resonance targets. Invoke when asked to visualize Rife frequencies, plasma tube resonance, MOR fields, or morphogenic frequency-matter interactions in 3D.
---

# Rife Resonance Visualizer

Produces a real-time 3D visualization of Royal Raymond Rife's plasma tube resonance system — the characteristic plasma tube emission, the frequency-specific standing wave field it generates, the cellular-scale resonance targets, and the spectral decomposition of the MOR (mortal oscillatory rate) frequencies — using Three.js r182+, React Three Fiber v9, TSL shaders, and GPU particles.

## When to Use

- User asks to visualize Rife frequencies, Rife plasma tube emission, or MOR resonance fields
- User wants a 3D rendering of a plasma tube resonator with animated frequency field output
- An interactive demonstration of standing wave resonance patterns at multiple frequencies is needed
- User is building an educational tool around Rife's microscopy experiments or frequency-medicine claims
- User wants to render spectral emission lines, plasma glow, or wave-interference standing patterns in 3D

## Process

1. **Plasma tube geometry**:
   - Model the Rife plasma tube as a `CylinderGeometry` (elongated, low radius) with rounded end-caps using `SphereGeometry` hemispheres merged into a `BufferGeometry`
   - Apply a volumetric glow `ShaderMaterial` that raymarches a cylindrical density field: the plasma density `ρ(r) = ρ₀·e^(−r²/σ²)` gives a bright axial glow fading to dark at the walls
   - Animate plasma `σ` (beam width) pulsing with `sin(time·frequency)` to simulate the RF-driven plasma discharge

2. **MOR frequency standing wave field**:
   - Extend a standing wave field from each electrode of the tube outward as concentric `RingGeometry` pairs oscillating in antiphase (nodes and antinodes alternating)
   - Compute antinode positions: `z_antinode = n · λ/2` for harmonic `n`; render each antinode as a bright ring, each node as a dark ring
   - Animate the rings with `amplitude = A·sin(2π·frequency·time − k·z)·sin(k·z)` — the standing wave envelope

3. **Spectral emission color mapping**:
   - Map each selectable MOR frequency to a visible-spectrum color using the standard wavelength-to-RGB approximation (encoded as a `DataTexture` LUT)
   - Change the plasma tube color and standing wave ring color dynamically when the `frequency` control is adjusted
   - Display a 2D frequency spectrum bar chart as a `PlaneGeometry` + `ShaderMaterial` showing harmonic decomposition

4. **Cellular resonance target visualization**:
   - Render 500 microscale cellular `SphereGeometry` targets randomly distributed in a cylindrical volume around the tube
   - When a cell's resonance frequency matches the selected MOR, animate it with a `scale` pulse (`scale = 1 + 0.4·sin(time·MOR_freq)`) and change its color from neutral grey to glowing red-orange
   - Use `InstancedMesh` for the 500 cells with per-instance color and scale encoded in the instance matrix and a color `Float32Array` attribute

5. **Fourier decomposition overlay**:
   - Render a real-time Fourier decomposition of the standing wave as 12 sinusoidal `TubeGeometry` overlays at decreasing opacity — the first harmonic brightest, higher harmonics dimmer
   - Animate each harmonic independently: `y(t) = (A/n)·sin(n·2π·frequency·time)`

6. **Post-processing**:
   - `Bloom` (threshold 0.15, intensity 3.0) for the plasma glow and resonating cells
   - `GodRays` from the plasma tube axis
   - `ColorGrading` toward a warm-amber palette to evoke Rife's period laboratory aesthetic

7. **Runtime controls (lil-gui)**:
   - `frequency_hz` (20–1 000 000 Hz, logarithmic scale) — the primary MOR frequency
   - `plasma_power` (0–1) — scales plasma density and emission intensity
   - `harmonic_count` (1–12) — number of Fourier harmonics displayed
   - `cell_count` (50–1000) — number of cellular resonance targets
   - `show_standing_waves`, `show_cells`, `show_spectrum_display`, `show_fourier_harmonics`

## Output Format

```
RifeResonanceScene/
├── RifeResonanceScene.jsx
├── components/
│   ├── PlasmaTube.jsx           ← Volumetric raymarched tube shader
│   ├── StandingWaveField.jsx    ← RingGeometry node/antinode animation
│   ├── SpectralColorMap.jsx     ← DataTexture frequency-to-color LUT
│   ├── CellularTargets.jsx      ← InstancedMesh cells with resonance pulse
│   ├── FourierHarmonics.jsx     ← TubeGeometry sinusoidal overlays
│   └── PostFX.jsx
├── shaders/
│   ├── plasmaGlow.tsl.js       ← TSL cylindrical raymarched plasma
│   └── standingWave.tsl.js     ← TSL standing wave node/antinode
└── controls/gui.js
```

## Boundaries

- Do NOT present Rife's MOR frequencies as medically or scientifically validated — clearly label all frequency-resonance effects as Rife's historically documented experimental claims, not peer-reviewed therapeutics.
- Do NOT suggest the visualization constitutes medical or health advice.
- Do NOT recreate geometry per frame — reuse all `BufferGeometry` attributes.
- Present Rife's work in its 1930s historical context as microscopy and RF experimentation.
