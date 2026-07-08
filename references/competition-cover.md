# Competition / Showcase Cover

Use this for competition entries, hackathon submissions, portfolio/showcase covers, product demo thumbnails, award-style project posters, and first-screen visual assets for a completed work. This reference captures the successful "particle system showcase cover" look: polished, cinematic, product-like, and visually complete.

This is **not** a generic technical blog cover. A competition/showcase cover should sell the work in one glance: what the project feels like, what its signature interaction is, and why it looks finished.

Load first:
- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

---

## Defaults

| Field | Value |
|---|---|
| Output directory | `~/Pictures/better-image-gen/` unless the caller gives a project path |
| Final format | `.webp` |
| Quality | q78 |
| Primary size | `1280x720` |
| Model flow | GPT primary → GPT retry → Gemini → Doubao |

For competition/showcase covers, prefer landscape:
- `1280x720` for normal web cards, README heroes, blog covers, and project gallery cards.
- `1536x864` or `1920x1080` when the cover is the main submission hero.

---

## Visual Recipe

The cover should feel like a polished project still, not a diagram.

Use this composition:

1. **Hero object** — the actual product surface, app window, game scene, installation, canvas, device, dashboard, or artifact being showcased.
2. **Signature effect** — the unique interaction or visual behavior: particles, confetti, live data, agent traces, animation trails, glowing states, generated assets, or gameplay motion.
3. **Stage environment** — a cinematic background, desktop context, subtle glass floor, floating panels, or atmospheric depth that frames the work.
4. **Visual hierarchy** — one clear focal point, supporting secondary details, clean negative space for optional title overlay.
5. **No rendered text** — never rely on the image model to draw titles or labels. Add copy later in design or in the webpage.

Good showcase concepts:
- "macOS utility celebration effect showcase"
- "particle system UI effect presented as a polished app demo"
- "AI agent dashboard as a finished product hero"
- "hackathon project cover with app surface and signature interaction"
- "creative coding canvas with final animation state"
- "product demo card with floating UI and live effect"

Avoid:
- generic AI/cyber wallpaper with no product subject
- tutorial-like diagrams
- cluttered screenshots pasted into a collage
- readable fake code or fake labels
- brand marks, platform logos, exact UI trademarks
- overly literal trophies, medals, fireworks, or marketing badges unless the user explicitly asks

---

## Prompt Structure

Use this structure:

```text
Landscape competition showcase cover for {project/work}.
A polished {hero object} demonstrating {signature effect}.
The scene presents the finished work as a cinematic product demo: {stage environment and supporting details}.
{palette and lighting}.
High-end portfolio quality, strong first-glance impact, clean negative space, no text, no letters, no watermark, no brand marks, no platform logos.
```

For Chinese requests, keep the outbound image prompt in English for model reliability, but preserve Chinese file names and response language.

---

## Particle / Confetti Showcase Template

Use this when the submitted work is an animation, UI effect, particle system, celebration interaction, creative coding piece, or visual-feedback feature.

```text
Landscape competition showcase cover for a macOS utility feature: a rank-up celebration particle effect.
A polished dark translucent macOS-style app surface floats above a soft desktop scene, surrounded by bright confetti rectangles, circular chips, diamond glints, subtle bloom halos, and elegant motion traces.
The image presents the finished work as a cinematic product demo: visible particle layers, emitter energy, crisp glass UI, and a celebratory full-screen moment captured at its peak.
Qingshan Lake inspired palette: deep cypress green, lake teal, mist white, subtle dawn gold, plus vivid celebration particles.
High-end portfolio quality, strong first-glance impact, clean negative space, cinematic lighting, high contrast particles, no text, no letters, no watermark, no brand marks, no platform logos.
```

Why this works:
- "competition showcase cover" tells the model this is a finished project hero, not documentation.
- "polished app surface" creates a concrete product subject.
- "captured at its peak" makes the output feel like a selected hero frame.
- "visible particle layers" keeps the generated result tied to the actual feature.
- The palette constraint avoids generic neon tech imagery.

---

## Product / App Showcase Templates

### AI Agent Product

```text
Landscape competition showcase cover for an AI agent productivity app.
A polished translucent desktop app window floats in a cinematic workspace, showing abstract agent activity as branching task paths, tool-call pulses, compact cards, and glowing state transitions.
The scene presents the finished work as a premium product demo: calm control surface, visible automation flow, precise UI hierarchy, and subtle depth.
Deep graphite, lake teal, mist white, restrained dawn gold highlights, high-end portfolio quality.
clean negative space, no text, no letters, no watermark, no brand marks, no platform logos.
```

### Data / Dashboard Product

```text
Landscape competition showcase cover for a data dashboard product.
A refined glass dashboard floats above a dark workspace, with luminous charts, compact metric cards, flowing data paths, and subtle animated signal traces.
The image feels like a finished SaaS product hero: information-dense but calm, premium, precise, and ready for a demo.
Deep cypress green, graphite, lake teal, mist white, small warm highlights, cinematic depth of field.
clean negative space, no text, no letters, no watermark, no brand marks, no platform logos.
```

### Creative Coding / Visual System

```text
Landscape competition showcase cover for a creative coding visual system.
A luminous canvas installation floats in a dark studio, showing layered particles, vector fields, orbiting chips, soft glints, and generative motion trails.
The scene presents the artwork as a completed interactive piece: crisp visual structure, expressive motion frozen at the best moment, gallery-quality lighting.
Deep graphite, lake teal, mist white, vivid accent particles, restrained warm glow.
clean negative space, no text, no letters, no watermark, no brand marks, no platform logos.
```

---

## Pipeline

Use the standard single-image pipeline from `references/portrait.md`, with:

```bash
REQ_SIZE="${REQ_SIZE:-1280x720}"
POSTPROCESS_NOTE="competition showcase cover webp q78"
```

If saving into a project/blog/repo, place the final WebP under the target image directory, for example:

```bash
FINAL_PATH="/path/to/project/assets/{slug}.webp"
```

Always write the metadata JSON next to the final image.

---

## Quality Checklist

Before accepting the image:

- It should look like a finished project hero, not a tutorial illustration.
- The work/product must be the first-viewport focal point.
- The signature interaction/effect should be visible without explanatory text.
- There should be one clear hero object and a controlled supporting environment.
- The image must work without any rendered words.
- The result should avoid generic AI wallpaper aesthetics.
- The color palette should have a restrained base plus high-contrast accents.
- There should be enough clean space for optional overlay copy in the final layout.
- File size should normally stay below 300 KB after WebP conversion.

