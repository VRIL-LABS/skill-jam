---
name: paper-shaders
description: Minimal guidance for creating paper-inspired shader effects and visual treatments using the official paper-design/shaders docs and examples. Invoke when a user wants paper-like gradients, texture layers, grain, noise, soft translucency, or shader-backed design patterns grounded in the official docs.
---

# Paper Shaders

This is a minimal hand-rolled skill that points at the official `paper-design/shaders` documentation and examples instead of a personal fork or thin auto-generated package.

Use it when the task is to design paper-like textures, subtle shader backgrounds, grainy overlays, or procedural design treatments for websites, interfaces, or generative art.

## When to Use

- User asks for paper-texture, shader, or paper-inspired visual effects
- Project needs soft grain, layered gradients, subtle motion, or stylized translucent surfaces
- User wants a design system-like background that feels tactile but still performant
- The task needs a grounded implementation strategy based on the official docs, not an unmaintained third-party fork

## Process

1. **Confirm the stack** — determine whether the scene is plain CSS, WebGL, Three.js, React, or a design mockup.
2. **Check the official repo docs** — use the `paper-design/shaders` README and its examples as the primary source of truth.
3. **Choose the minimal pattern** — prefer a single, readable shader or texture treatment over a heavy custom pipeline.
4. **Adapt to the project** — translate the official effect into the active framework while preserving naming, performance, and readability.
5. **Keep it editable** — expose only the key parameters needed for tuning: grain, softness, palette, motion, and contrast.
6. **Verify output quality** — review the result against the design goal and ensure it remains readable and performant.

## Recommended Sources

- Official repo: `https://github.com/paper-design/shaders`
- Official docs/README: use the repo landing page and linked examples as the canonical reference

## Boundaries

- Do NOT invent a custom shader system when the official docs already provide the appropriate pattern.
- Do NOT rely on random personal forks or unmaintained packages when a direct official source exists.
- Do NOT add heavy post-processing or expensive effects unless the project explicitly requires them.
- Do NOT overspecify the design; the goal is subtle material realism and polished texture treatment, not visual noise.

## Output

Provide:

- the selected shader or paper texture pattern
- the minimal configuration needed to integrate it
- any caveats about browser support, performance, or asset tuning
- a short explanation of why the effect matches the design intent
