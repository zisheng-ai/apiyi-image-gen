# Codex-Compatible Animated Pets

Use this workflow for a **new Codex custom pet**, a repair of an existing pet, or an upgrade from a standard 8×9 atlas to a v2 8×11 atlas. It is deliberately stricter than `sprite-loop.md`: a pet is an interaction contract, not just a pleasing animation.

Load first:

- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

Do not reduce a pet request to a generic 12-frame sprite loop.

## Delivery Boundary

- Deliver a package folder only; never write to, install into, register with, update, or delete `~/.codex/pets`.
- Do not click Codex/Owlet installation or update UI on the user's behalf.
- A final package contains `spritesheet.webp` (or lossless `spritesheet.png`), `pet.json`, and QA artifacts. Keep the working run outside Codex state, defaulting to `~/Pictures/better-imagegen/codex-pet/<pet-id>/`.
- Preserve user-provided art, valid existing rows, and approved identity cues. Do not silently restyle a repair.

## V2 Geometry and Manifest

| Item | Required value |
|---|---|
| Cell | `192×208` px |
| Columns | 8 frames per row |
| Standard rows | 9 (`0...8`) |
| Look rows | 2 (`9...10`) |
| Final atlas | `1536×2288` px / 8×11 |
| Intermediate atlas | `1536×1872` px / 8×9; never package it as new work |
| Manifest | `spriteVersionNumber: 2` |

Minimum `pet.json`:

```json
{
  "id": "friendly-kebab-case-id",
  "displayName": "Friendly Pet",
  "description": "One short user-facing sentence.",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.webp"
}
```

## Required Rows

Rows 0–8 each contain eight sequential frames. Generate an entire row as one coherent strip; do not combine one-off cells from unrelated generations.

| Row | State | Required behavior |
|---:|---|---|
| 0 | `idle` | Calm micro-variation only: blink, breath, tiny bob, small material sway. Must not be visually static. |
| 1 | `running-right` | Clearly faces and travels screen-right; alternating gait; no speed lines, dust, shadow, or trail. |
| 2 | `running-left` | Clearly faces and travels screen-left; may mirror approved `running-right` **frame-by-frame without reversing time** only when markings, props, lighting, and semantics remain valid. |
| 3 | `waving` | Limb/wing gesture only; no wave marks or floating effects. |
| 4 | `jumping` | Vertical motion through body position only; no floor/shadow/dust/landing cue. |
| 5 | `failed` | A legible failure reaction. Only small opaque, attached tears/smoke/stars are permitted when physically connected. |
| 6 | `waiting` | Distinct expectant/help-needed pose, not ordinary idle. |
| 7 | `running` | Focused working/thinking/processing state; never literal jogging or directional travel. |
| 8 | `review` | Focus through eyes, head, lean, or limb; no newly invented documents, magnifiers, UI, or text. |

The state action must carry the animation. Avoid detached effects, speed lines, afterimages, blur, glows, shadows, scenery, readable text, guides, labels, grids, or cell-crossing elements. Keep one centered whole-body pose in each slot with an empty gutter and safe padding.

## Identity, Transparency, and Grounding

1. Generate or choose exactly one canonical base image first. It locks face, body proportion, material, palette, markings, prop design, and silhouette.
2. Every later row uses the canonical base and all user references that define identity. Text-only row generation without visual grounding is invalid.
3. Use a flat chroma-key background during row production, or genuine alpha when reliable. The final atlas must have transparent outside regions.
4. Keep the pet compact and readable in a `192×208` cell. Do not depend on tiny details or soft effects.
5. Inspect alpha/matte cleanup at normal pet size and on light, dark, and checkerboard backgrounds. Remove only edge-connected background; preserve hair/fur/antialiased silhouette. Never feather pixel art.
6. A transparent interior hole is only valid when it belongs to the design (for example, a ribbon loop). Reject accidental seams, sliced bands, scanline gaps, and see-through filled body parts.

## Look-Direction Contract (Rows 9–10)

Rows 9–10 are mandatory for every new v2 pet. They are a continuous clockwise gaze/orientation family—not neutral poses and not a turntable unless the pet is literally a rigid rotating object.

```text
row 9:  000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5
row 10: 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5
```

- `000` means **up**, not neutral/front. Neutral input falls back to idle unless the renderer offers a dedicated neutral cell.
- Directions use viewer/screen coordinates: `090` is screen-right and `270` is screen-left.
- First generate and approve one four-cardinal strip: `000` up, `090` right, `180` down, `270` left. If any cardinal is ambiguous, repair it before either look row.
- Then generate row 9 as one coherent eight-pose family. Generate row 10 only after row 9 has passed registration, edge, semantic, and continuity checks.
- Each 22.5° step must advance naturally. Check row boundaries `157.5 → 180` and `337.5 → 000` as carefully as within-row pairs.
- Keep an anatomical/physical anchor stable—normally feet, lower body, base, or torso. No unexplained scale pop, baseline drift, lateral slide, flipping, or prop teleportation.
- Never fake look direction with whole-sprite rotation, whole-cell rotation, skew, or arbitrary affine warp. Use the pet's real mechanics: eyes/head/ears/body bend/feature surface/props as appropriate.

Before generation, write a concise `look-mechanics.md`: what is anchored; what leads gaze; what follows; how eyes, eyelids, head, body, appendages, and props behave at all four cardinals; and the per-step motion budget. Preserve the original eye construction—no pasted googly eyes or un-clipped pupil dots. For humanoids, use restrained eye + eyelid/brow + head/neck + upper-body follow-through without deforming anatomy; for flexible objects, bend/aim their natural upper feature while anchoring the base; for screen/sticker faces, changing drawn features may be appropriate.

## QA Gates

Do not package until every gate passes.

1. **Row QA:** exactly 8 separated poses per strip; no clipping, slot overlap, blank frame, detached fragment, guide mark, identity drift, incorrect state, or broken gait.
2. **Motion QA:** inspect contact sheet and per-row preview GIFs. Reject size popping, baseline jumps, static idle, reversed cadence, wrong directional facing, or a generic `running` row that literally runs.
3. **Directional QA:** verify each cardinal at normal pet size. Independently blind-review the 16 direction cells with three reviewers when available; cardinal ambiguity is blocking. An intermediate uncertainty may be accepted only when labeled ordered review confirms the intended quadrant and an explicit minor-warning record explains why.
4. **Continuity QA:** compare every adjacent direction pair, including both row joins. Reject wrong quadrant, reversal, conspicuous snap, identity/scale change, broken attachment, or registration jump.
5. **Raster QA:** verify the final atlas is exactly `1536×2288`, all used cells are non-empty, unused cells are fully transparent, and no opaque chroma-key pixels or accidental interior holes remain. Apply one deterministic edge-local despill pass only; do not repeatedly regenerate art for chroma fringe once that pass and validation succeed.
6. **Final visual QA:** inspect the 11-row contact sheet plus motion previews at actual pet scale. A technically valid atlas with unreadable directions or inconsistent character identity fails.

For a failed generated row, classify the root cause before retrying: visual semantics, identity, geometry/clipping, component connectivity, extraction, chroma, or continuity. Fix deterministic failures deterministically; regenerate only when the source art is wrong. After two retries with the same root cause, change strategy—strengthen cardinal anchors, simplify the pose/prop, or revise mechanics—instead of endlessly varying the prompt.

## Output Checklist

```text
<pet-id>/
  spritesheet.webp | spritesheet.png
  pet.json
  qa/
    contact-sheet-extended.png
    look-directions.png
    review.json
    direction-semantics.json
    direction-blind-*.json          # when blind review is used
    look-continuity.json
    chroma-despill-extended.json
    run-summary.json
    previews/*.gif
  validation-extended.json
```

`run-summary.json` must identify the final spritesheet, manifest, validation, despill report, contact sheet, direction sheet, motion previews, and final verdict. Report the package and QA paths to the user. Do not claim installation or dynamic in-app verification; those steps belong to the user.

## Existing Pet Repair / Upgrade

- A valid 8×9 atlas may be treated as approved rows 0–8 only after deterministic and visual validation; add the two look rows and package v2.
- For a valid v2 atlas, preserve approved standard rows. Repair the **whole containing row** when a generated look row is wrong; never place an unrelated one-off repair cell among a coherent row.
- Use the atlas or an approved idle/default cell as canonical identity reference. Include all material, face, marking, prop, and look-mechanics references in repair generation.
