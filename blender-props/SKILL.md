---
name: blender-props
description: Create or revise simple 3D game props in Blender from descriptions or visual references, including materials, basic mechanical rigs, preview renders, and FBX delivery for Unity. Use for furniture, books, lamps, and similar props; Unity scene integration is a separate step when requested.
---

# Blender Props

Produce editable models and inspectable exports from the user's references. Use Blender's Python API through its executable when shell access is available; no Blender MCP server or paid generation service is required for this workflow.

## Establish the asset contract

- Read the project's asset conventions and inspect the supplied images. Separate shape, colour, material, and logo references; identify which surface should receive each graphic.
- Determine real-world scale, pivots, intended viewing distance, moving parts, and delivery formats from the request and project. State reasonable assumptions for unspecified visual details and proceed; ask only when missing information materially changes the model.
- Honour the user's Blender executable path. Otherwise check PATH and plausible installations, then run `--version`. Record the actual version; do not install or upgrade Blender as a side effect of modeling.
- Work in an asset-specific directory. A useful default is `ArtSource/<AssetSet>/` with a build script, `.blend`, `Textures/`, `Exports/`, and `Previews/`. Keep `.blend` outside Unity's `Assets` unless direct Blender import is intentional. Avoid overwriting an artist-edited source with a procedural rebuild.

## Build and shade

Create a reproducible `bpy` script for procedural props, resolving paths relative to the script and using a fixed seed when randomness affects geometry. For revisions to an existing hand-authored `.blend`, preserve its contents and work on a copy instead of rebuilding unrelated objects. Run scripts with `--python-exit-code 1` before `--python` so Python failures are visible to the caller. See [Blender execution and FBX notes](references/blender-fbx.md) for tested commands and export details.

Use named objects/collections, intentional pivots, consistent metre units, applied mesh scale before beveling, and enough geometry for the actual camera distance. Prefer a small number of material slots and mesh objects; do not join meshes at the cost of losing independent animation or editing controls. Report triangle and material counts rather than claiming mobile performance from polycount alone.

Match silhouette and proportions first, then material colour and surface detail. Inspect wood grain at the scale of the whole prop: grain should follow planks and legs, UV repetition should not introduce obvious seams, and contrast should match the reference. Prevent overlapping coplanar layers and inspect bevel/cap normals, especially around reflective metal and thin lamp shades.

Procedural Blender shaders do not automatically become Unity materials. Bake important procedural colour detail to image textures with UVs; include normal/roughness maps only when needed. Pack textures in the `.blend` and deliver image files alongside FBX. Use supplied logos as supplied when appropriate; disclose whether they sit on an inset or have transparency. Never silently stretch a reference screenshot containing unrelated UI into a texture.

## Rig only the requested motion

For a hinged prop, use meaningful root/hinge bones and explicit skin weights. Make the rotation axis and pivot intentional. A book may need page flattening and a deforming spine as well as a cover rotation; verify their combination instead of assuming a rigid hinge alone closes correctly.

Bake the intended motion to a named action. Keep FPS, duration, start/end poses, and manual controls documented. If closure uses shape keys, export and verify their animation together with the bones. Check intermediate poses for intersections, gaps, detached parts, and unnatural stretching. Do not add page turning or character-rig complexity to a request for simple opening/closing.

## Export and verify

Export each requested prop from its intended origin, before applying presentation-only placement. Include only the needed meshes and armature; keep studio lights, cameras, floor, and other props out of an individual asset's FBX. Use explicit axis/unit settings and disable unwanted leaf bones or unrelated animation takes. Preserve shape keys when choosing modifier/export settings.

Verification has three separate levels:

1. **Source and visuals:** open/save the `.blend`, render the whole prop and relevant details/states, inspect the images, and correct visible issues. Check external files or packed textures actually resolve.
2. **FBX round trip:** import each export into a fresh Blender scene. Verify scale, geometry, materials/textures, and, when animated, bones plus deformed geometry at the endpoints and representative intermediate times. Match FPS and time origin before comparing poses; FBX import can add a frame offset. UV seams may split vertices, so raw vertex-count equality alone is insufficient.
3. **Unity integration:** when requested and authorized by project rules, use the Editor to import, configure the appropriate rig and render-pipeline materials, and inspect playback. Let Unity own `.meta`, `.mat`, `.prefab`, and `.unity` serialization. A successful Blender round trip does not verify Unity's importer or shaders; report Unity verification as pending when it was not performed.

After the relevant checks pass, deliver links to the `.blend`, exports, textures, previews, and a short asset-specific usage note. Explain the animation controls and any material remapping still needed. Report what was checked and what remains unverified. Do not modify gameplay, Addressables, or scene flow merely to deliver a model.
