# Blender execution and FBX notes

Read this when writing a build script, exporting animation, or diagnosing a round-trip mismatch. This workflow was exercised with Blender 5.2.3 LTS on Windows for a table, a hinged book, and a lamp. It is a tested version, not a required version or a claim that other releases were checked. Use the installed Blender API as the source of truth when adapting snippets.

## Execute a build

PowerShell, using the user's executable path:

```powershell
$blenderExe = 'E:\Utilities\Steam\steamapps\common\Blender\blender.exe'
& $blenderExe --version
& $blenderExe --background --python-exit-code 1 --python 'ArtSource/MyProps/build_props.py'
if ($LASTEXITCODE -ne 0) { throw 'Blender asset build failed' }
```

Equivalent with an executable already on PATH:

```bash
blender --background --python-exit-code 1 --python ArtSource/MyProps/build_props.py
```

Blender arguments are processed in order. Set the nonzero Python exit code before running the script. A clean process exit without that option does not reliably prove that a Python script completed. Check completion output and expected files as well.

Use `Path(__file__).resolve().parent` for asset-relative paths. Only use `bpy.ops.wm.read_factory_settings(use_empty=True)` in a fresh procedural build or an isolated verification process, never as the first operation when the task is to edit an existing scene. Put baking image files, logs, and previews in the intended asset/work directory. Preserve hand-authored sources when rerunning a generator.

## Export parameters

Select only the prop's meshes and, if animated, its armature. Set an active selected object. Start with these settings and adapt them to the asset contract:

```python
bpy.ops.export_scene.fbx(
    filepath=str(export_path),
    use_selection=True,
    object_types={'MESH', 'ARMATURE'},
    axis_forward='-Z',
    axis_up='Y',
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_UNITS',
    use_mesh_modifiers=not has_shape_keys,
    mesh_smooth_type='FACE',
    add_leaf_bones=False,
    bake_anim=animated,
    bake_anim_use_all_actions=False,
    bake_anim_use_nla_strips=False,
    bake_anim_force_startend_keying=True,
    bake_anim_simplify_factor=0,
    path_mode='COPY',
    embed_textures=True,
)
```

This is a parameter example, not a complete export script; `export_path`, `has_shape_keys`, and `animated` come from the actual asset. Before exporting shape keys, apply required topology-changing modeling modifiers while it is still safe to do so. Exporting an evaluated/modifier-applied mesh can lose its blend shapes; disabling modifier export preserves them but does not apply required modeling modifiers for you. Keep armature skinning and inspect the exported result.

Avoid relying on arbitrary Blender node graphs, bump nodes, constraints, drivers, or studio illumination surviving FBX. Bake what the engine needs. Provide the source images even when embedding them. Static props need no animation export. A non-humanoid prop rig usually uses Unity's Generic rig type; verify the actual imported hierarchy and take names in the target Editor.

## Animation round trip

Capture evaluated mesh positions from the source at the opening pose, intermediate times, and the closed pose. Use a fresh scene/process for import, matching the source FPS:

```python
bpy.context.scene.render.fps = source_fps
bpy.ops.import_scene.fbx(
    filepath=str(export_path),
    use_anim=True,
    anim_offset=0,
)
```

The tested Blender importer otherwise added one frame. That made intermediate bone/shape-key poses disagree even though the exported animation was correct. Check the installed importer's options and align by time instead of accepting a large positional tolerance to hide an offset.

Evaluate armature deformation and shape keys through the dependency graph. Compare positions in the same coordinate space, accounting for presentation-only offsets and axis conversion. FBX may split vertices at UV/material/normal boundaries; compare geometry spatially rather than requiring identical vertex indices. For small metre-scale props, a tolerance around `0.0001` m can catch visible export errors while tolerating float conversion; choose a tolerance appropriate to asset size. Check both directions of a spatial comparison so missing geometry is not overlooked.

Record which files and frames were checked, the measured error, and whether textures, bones, and shape keys survived. Successful import alone does not establish animation equivalence. Inspect renders separately: a mathematically preserved rig can still look wrong or intersect in the original source.

## Unity handoff

Keep source `.blend` files outside `Assets` for explicit FBX delivery. Import only the chosen exports/textures when integration is in scope. Use the project's actual render pipeline; for URP, assign suitable URP materials through the Editor and map the baked textures explicitly. Blender roughness and Unity smoothness use opposite conventions; check values and map channels instead of assuming texture equivalence. Confirm scale, normals, pivot, clip timing, blend shapes, material appearance, and relevant end/intermediate poses in Unity before claiming engine validation.
