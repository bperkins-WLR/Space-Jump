# Cloud Hopper

A small 3D platformer built with Three.js — pick an animal and hop across floating platforms above a sea of fluffy clouds, collecting golden rings and power-ups through five themed worlds. Plays in any modern browser and is installable to the iPhone/iPad home screen as a PWA.

## Play

Open `index.html` in a browser, or visit the deployed site.

### Controls

**Keyboard**
- `W` / `↑` — forward
- `A` / `D` — strafe left / right
- `Space` — jump (hold for higher · tap again mid-air for double jump)

**iPad / touch**
- On-screen D-pad (bottom-left) for movement
- Big JUMP button (bottom-right)
- In Safari, tap **Share → Add to Home Screen** for a full-screen install

## Features

- Three.js 3D scene with shadows, fog, and a starfield
- Animated rippling lava with point-light glow
- Procedurally generated platforms with difficulty ramp every level
- Spikes, collectible coins, particle bursts, moving platforms at L4+
- Synthesized SFX (Web Audio API — no asset files)
- Coyote time, jump buffering, variable jump height, double jump
- Touch controls + iOS PWA meta tags

## Tech

Single static HTML file. Three.js is loaded from unpkg via CDN, so there's no build step.

## Deploy

Static — drop it on Vercel, Netlify, GitHub Pages, or any CDN.
