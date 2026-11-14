---
name: unity-ui-assets
description: Turn a game UI screenshot, mockup, or art reference into a layered set of Unity PNG sprites with style-matched extraction, reconstruction, selective regeneration, and a before-and-after gallery. Use for new screens or targeted revisions to an existing sprite pack.
---

# Unity UI Assets

Use `$unity-ui-assets` with a reference image, the desired output folder, and any layout or style constraints. If the user asks for a breakdown first, deliver the breakdown and wait for the go-ahead before running generation.

## Inventory the screen

- Inspect the full reference and zoom in on layered or ambiguous parts. Give each visible element a stable ID, a source crop, a layer or z-order, an intended use, and a treatment: `EXTRACT`, `RECONSTRUCT`, `GENERATE`, or `LIVE_UI`.
- Map reusable artwork to one sprite ID with multiple placements. Split elements that must move, resize, recolor, or swap independently. Keep fixed decoration together when it will always move as a unit. Record what is obscured and what needs to be inferred.
- Record a shared style brief from the reference covering palette, silhouette, proportions, lighting, bevels, line weight, material, and shadow treatment. Keep labels, values, and localized text live in Unity. Retain lettering in brand artwork only when the user wants it baked into the logo.

## Produce assets

- **Extract** visible elements from source pixels with an explicit mask. Preserve cutouts and intentional details. For a recognizable character, retain the original face when the reference permits a usable cutout.
- **Reconstruct** occluded or text-covered regions from the existing art and neighboring material. Keep shared geometry for layers that must align, such as a book shell, pages, and bookmark. Rebuild repeated geometric surfaces once.
- **Generate** missing elements or parts that need more reconstruction than the source supports. Reuse a working image-conditioned workflow, such as GameArt UI Asset Extract in ComfyUI, when available. Queue one job per candidate with the relevant reference crop, a shared style brief, and a short asset-specific prompt covering shape, material, orientation, and the intended cutout. Save the original RGB, mask or initial RGBA, workflow, and seed when the backend exposes them. Check the local backend and installed model inputs before submitting jobs. If generation is unavailable, continue with extraction and reconstruction and report the generation jobs still pending.
- Use an installed cutout model for a first mask on isolated generations. Refine a rough boundary with a narrow contour band and clean background RGB from partially transparent pixels. For a small gold icon on a green plate, use the traced shape and local color contrast to remove fully opaque spill as well. For soft edges or low contrast, inspect the cutout on light and dark backgrounds and retain the best mask if automatic cleanup removes detail.

## Review and retry

Compare each candidate with its reference crop at native and intended display sizes. Check shape, palette, highlights, lettering where requested, transparent openings, stray pixels, halos, clipped edges, and padding. Assemble the screen from the exported layers to check alignment, reuse, and visual consistency. For stretchable panels, verify the fixed caps and safe stretch region. For fills, inspect low, medium, and full values.

After the initial attempt, allow up to **three retries per asset** by default. Stop early when a candidate passes. Fix mask or matte defects at the cutout stage, and change the crop or prompt for shape, style, or composition defects. Keep the best candidate across attempts. Reuse the reviewed exports for assets that pass. At the limit, mark unresolved assets `REVIEW` with the exact defect and the next action. For generation defects, include a proposed prompt or crop change. Follow a different limit when the user specifies one.

## Package the run

Use a separate output folder for the run. Preserve the previous pack as the comparison baseline. Export `Unity/` PNGs with intentional alpha and padding, a full-resolution source when useful, a layered assembly preview, `manifest.json`, and `QA.md`. The QA report lists checked properties, counts by status, unresolved assets, selected attempts, and specific follow-up actions. State whether the sprites were tested in the Unity Editor or only inspected as exported PNGs.

After every full breakdown or production run, deliver `Gallery.html`. Show the full reference beside the assembled screen and a labeled Before/After pair for each sprite. Use the previous PNG on the left or a labeled reference crop when there is no previous export. For mask comparisons, use the same underlying image, crop, scale, and preview background. For a breakdown-only request, show the source crops and a labeled layout preview made from those crops, with pending exports marked in the gallery. Check every local link and link the gallery in the handoff. Use the [manifest and gallery guide](references/run-manifest.md) to generate it. Write the QA report and handoff in the user's language.
