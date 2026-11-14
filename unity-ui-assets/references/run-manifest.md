# Run manifest and gallery

Keep one manifest per reference or revision. Use reference coordinates in pixels, measured from the top left. Crop bounds use `[left, top, right, bottom]` with exclusive right and bottom edges. Record positions for each placement even when several placements share one PNG. If padded source sprites need to align in a composite, record their padded top-left offsets. Record any 9-slice borders in exported Unity pixels, including transparent padding.

The gallery helper reads the image paths and status fields below. Other fields are available to the agent or existing batch scripts. The example shows one extracted icon, two placements, and an optional cutout comparison.

```json
{
  "title": "Adventure menu",
  "language": "en",
  "reference_image": "Reference.png",
  "reference_size": [1448, 1086],
  "assembled_image": "Preview/Assembled.png",
  "style_brief": "Warm cream paper, thin gold bevels, and green enamel with upper-left lighting.",
  "assets": [
    {
      "id": "menu_chevron",
      "method": "EXTRACT",
      "status": "READY",
      "crop": [1249, 284, 1269, 315],
      "placements": [{"x": 1249, "y": 284, "z": 8}, {"x": 1265, "y": 457, "z": 8}],
      "reference_crop": "Reference/menu_chevron.png",
      "previous_png": "Before/menu_chevron.png",
      "unity_png": "Unity/menu_chevron.png",
      "selected_attempt": 1,
      "issues": []
    }
  ],
  "cutout_comparisons": [
    {
      "id": "menu_chevron",
      "before_png": "Cutout/chevron-mask-before.png",
      "after_png": "Cutout/chevron-mask-after.png"
    }
  ]
}
```

Use run-relative file paths with forward slashes. Bring any previous PNGs shown in the gallery into the run folder so the delivery is portable. Omit `previous_png` to use `reference_crop`. For an inventory-only run, set `preview_is_layout` to `true`, set `assembled_image` to the layout preview, and omit `unity_png` for pending entries. Keep text entries in the inventory as `LIVE_UI`. The gallery only renders entries for image assets.

Use `READY` for visually accepted exports, `REVIEW` for exported candidates with outstanding defects, and `PENDING` for missing exports. For generated assets, record each attempted seed, prompt, workflow or settings, result file, and review. Store a `next_action` for unresolved entries. For cutout comparisons, export both RGBA versions from the same RGB canvas with matching dimensions and alignment.

From the skill folder, run the helper with Python 3.9 or later. It uses only the standard library and verifies every referenced image file before writing the page. Choose `en` or `ru` for the built-in captions. For other languages, adapt the captions to the user's language.

```text
python scripts/build_gallery.py /path/to/run/manifest.json
```
