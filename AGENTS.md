# AGENTS.md

This file provides the full engineering and workflow rules for OpenAI Codex. Read [README.md](README.md) for installation and update instructions.

## Scope and adaptation

AI-UnityPipeline is a toolkit of instructions and skills, not a Unity game. It has no Editor version, render pipeline, scenes, gameplay assemblies, or Unity build to run. When maintaining this repository, edit only the requested instructions, metadata, and supporting resources; validate Markdown links, skill frontmatter, YAML, and the final diff. Do not modify Unity projects elsewhere on the machine.

When copying these rules into a Unity project, adapt the target-project guidance below to that project's verified facts. Keep the scope distinction until adaptation is complete: do not treat missing Unity files in this toolkit as broken project wiring. The detailed engineering standards below are the user's established preferences, not disposable examples. Preserve them unless a verified project constraint or explicit user instruction is incompatible; document that incompatibility and its replacement. Do not install packages or refactor the project merely to make it fit these rules.

`AGENTS.md` and `CLAUDE.md` each contain the full rules and can be used independently. Keep their rule bodies synchronized whenever updating this repository. During project installation or an authorized update, apply matching adaptations to each installed file while preserving agent-specific instructions.

User instructions and environment permissions take precedence. Task-specific workflow requests can override defaults here, but do not override an explicit current restriction or grant unavailable access.

## Branches and commits

- Check Git status and actual local/remote branches before changing branches. Preserve unrelated or unfinished work; use a separate worktree when needed.
- Develop each feature in `feature/<short-name>` from the user-specified base or actual integration branch. Use `dev` where established; this toolkit currently uses `main`. Do not invent `dev` or a release branch.
- Keep the feature branch for review. When integration is requested, use a squash merge unless the target project specifies otherwise. The preferred integration/release split is `dev` / `master` where the project uses it; do not impose it on a checkout with different branches. Identify releases by the user's platform/version hierarchy without inventing an unrequested tag format. Push, pull request creation, and merge require task authorization.
- Use concise English commit titles: `feat:` for capabilities, `add:` for supporting files, `edit:` for changes and cleanup, and `fix:` for defects or optimizations. Exclude unrelated files and temporary results.

## Task scope, files, and verification

- Edit the file types needed by the authorized task. Documentation, YAML metadata, reports, tests, and test helpers are valid outputs; there is no code-only restriction on this toolkit.
- Invoking `feature-cycle` requests the whole workflow: implementation, functional checks, temporary tests and necessary temporary resources, Performance & Reliability Code Review, fixes, cleanup, final verification, and `Status.md`. Do not ask again merely because general defaults make tests optional.
- Outside `feature-cycle`, choose proportionate verification for the task; permanent unit tests are optional unless requested or required by the project. A request for `chat-notes` permits its Markdown summary, without code changes or Git mutations.
- Use available Editor/CLI/MCP or batch-mode tooling for an authorized Unity task. Do not impose a blanket ban on local compilation or testing. Preserve the user's open Editor and unsaved work; verify the target project before Editor operations.
- Report what actually ran and its evidence. If the Editor, license, test harness, profiler, or device is unavailable, record the limitation rather than claiming success. Static review does not establish measured performance.
- Follow the skill's own sequence and report requirements instead of duplicating them here. `feature-cycle` performs mandatory review after functional success and before temporary test cleanup and the final commit. If functional execution is blocked, a static review may still help, but does not satisfy the functional gate.

## Target-project guidance: adapt before applying

Use `ProjectSettings/ProjectVersion.txt`, `Packages/manifest.json`, `Packages/packages-lock.json`, relevant settings, and existing code to establish the following. Do not assume the source project's classes, paths, platforms, installed packages, or performance bottleneck.

### Preferred stack and compatibility

- Preferred stack: **Zenject** for dependency injection, **UniTask** for async work, **DOTween** for tweens, and **Addressables** for asset/scene loading. These are established, trusted choices; do not replace them or turn feature work into a general dependency audit.
- Verify package presence, resolved versions, and actual usage before applying package-specific instructions. If a package is absent or incompatible, adapt those instructions to the existing architecture and record the reason; do not automatically install a replacement or introduce the preferred package.
- Where UniTask is adopted, new async code uses **UniTask**, not raw `Task` or coroutines. Preserve cancellation and owner lifetimes. Where DOTween is adopted, follow the existing tween ownership and teardown conventions.
- Use the exact Editor version pinned in `ProjectSettings/ProjectVersion.txt` and APIs supported by the resolved packages. Do not assume that a Unity release implies a particular URP version, renderer, graphics API, or installed plugin.

### Code style

- **Strict Microsoft C# style.** Private fields are `_camelCase` with a leading underscore; use PascalCase for types, methods, and properties, and camelCase for parameters and locals. Use `readonly` wherever possible, Allman braces on their own lines, `var` for obvious local types, and expression-bodied members (`=>`) for one-liners.
- **Member order inside a type, top to bottom:** constants/`static readonly` → serialized/private fields → properties → events/Actions → constructor (plain or Zenject `Constructor()` initialization) → public methods → private methods. Keep new code in this order and mirror a neighboring service.
- **No defensive null-checks.** Do not guard required serialized/injected references with `if (_field != null)` or `x == null → return` just in case. A missing asset, unassigned inspector field, or forgotten binding must fail loudly (normally a `NullReferenceException`), rather than silently skipping required work.
- Write a null-check when `null` is a real, expected state the logic must branch on: no pooled instance yet, an intentionally unbound slot with a defined fallback, or a destroyed Unity object during a legitimate teardown/async completion path. Handle cancellation and ownership explicitly; do not use lifecycle concerns as a reason to hide required wiring failures.
- **Extensions go in the project's extensions folder**, default `Assets/Code/Extensions`, as `*Extensions` classes such as `TransformExtensions` or `NumericExtensions`. Put reusable helper/extension methods there rather than scattering them inline. Adapt the folder to the project's existing layout instead of creating a duplicate extension tree.
- Keep the project's established initialization idioms. Where plain classes use a manually called `public void Constructor(...)` initializer, follow it for similar classes; do not turn it into a real C# constructor as incidental cleanup.

### Architecture and core patterns

Apply these engineering preferences to new feature code where compatible with the target project. Preserve an incompatible established architecture and explain the adaptation; do not migrate unrelated code.

- **OOP / SOLID** are followed strictly. Prefer interface-based dependencies and DI; do not add runtime service locators or static singletons to a project built around injected services. Keep documented platform-integration exceptions narrow. If the existing project deliberately uses another composition pattern, follow it rather than installing Zenject or rewriting it.
- **Dependency direction:** preserve the preferred **Infrastructure → Services → Game Logic** layering where used, including runtime/editor assembly boundaries. Use the project's actual namespace and assembly definitions.
- **Composition root:** register new services and factories in the actual bootstrap installer/composition root. Preserve eager static-data availability and bind-time initialization when other services depend on it; do not move required initialization into an unrelated later phase.
- **State-machine flow:** navigation, menu/game transitions, scene/level loading, and win/lose flow go through the existing state machine. Do not bypass it with direct screen or scene changes when that breaks the project's lifecycle.
- **Service-per-feature:** use interface-first services, `IFooService` + `FooService`, injected via Zenject where present. The usual binding is `Container.BindInterfacesTo<FooService>().AsSingle()`; match the intended scope rather than assuming every service is global. Per-frame work uses `ITickable`, and required bind-time initialization uses the project's eager-resolve convention. Respect initialization, ticking, and disposal lifetimes.
- **Factories:** a complex entity gets a dedicated factory following the project's existing factory base. Where Addressables and Zenject are present, load through the asset provider, instantiate through `IInstantiator`, and apply base setup. Use `UniTask` for async factory methods where UniTask is adopted. Trivial widgets can use the existing general/UI factory. Ask when the distinction affects the design and cannot be established from the project.
- **Asset and save abstractions:** use the established asset provider, resource-path constants, static-data services, and save facade. Add a missing path constant instead of multiplying inline Addressables/Resources strings. Preserve ownership, scene-cache cleanup, persistent-cache policy, and release rules actually implemented in the project; do not assume an API or class name exists.
- **Folders:** the original preferred layout is `Assets/Code` for runtime/editor code, `Assets/Tests/{EditMode,PlayMode}` for tests, `Assets/Resources/StaticData` for synchronous configs, and a dedicated addressable-content tree. Adapt actual paths and assembly boundaries at installation; do not assume those folders or the source project's spelling exist.

### UI

- Preferred stack: **uGUI** for runtime UI, with `RectTransform` and DOTween where adopted; **UI Toolkit** for editor tooling unless the user or existing project specifies otherwise. Adapt to an established UI Toolkit runtime, IMGUI editor, or inspector-only workflow without introducing a second UI system.
- New UI follows **MVVM**, with VM meaning presenter/presentation model:
  - **View** displays presentation data and may own its visual animation; no business logic.
  - **ViewModel/presenter** pulls model data, computes presentation-ready values, and feeds the View.
  - **Model** owns and serves the underlying data.
- Apply MVVM to **new UI only** where compatible. Preserve existing window/state abstractions and do not migrate existing screens or force a conflicting pattern into the project without an explicit requirement.

### Shaders and rendering

**Adapt pipeline-specific rules before use.** Identify the active Render Pipeline, renderer mode, resolved package versions, shader folders/names, platforms, and graphics APIs. The source project's URP Forward, shader paths, and Android/TV targets are not facts about another project. Keep the engineering restrictions below unless actual incompatibility requires a documented adaptation.

- **Shader organization:** the preferred source layout is `Assets/Code/Shaders`, with URP shader names `Custom/URP/<Name>`. Adapt the folder and naming to the target project's established layout and pipeline; do not create a duplicate shader tree.
- **HLSL and pipeline compatibility:** for URP, use the `"RenderPipeline" = "UniversalPipeline"` tag, `HLSLPROGRAM`, and includes from `Packages/com.unity.render-pipelines.universal/ShaderLibrary/`. Do not introduce Built-in `UnityCG.cginc`, `UnityObjectToClipPos`, `fixed4`, or surface-shader conventions into URP shaders. For Built-in or HDRP, use that pipeline's supported conventions; never impose URP tags, includes, or renderer APIs on them.
- **SRP Batcher:** where applicable, put material numeric properties in a single `CBUFFER_START(UnityPerMaterial) … CBUFFER_END` with a compatible layout across passes; textures/samplers remain in their appropriate declarations. If SRP Batcher compatibility is required, do not drive per-instance values through `MaterialPropertyBlock`; use appropriately shared/separate materials with explicit ownership and disposal. Adapt this policy for a verified incompatible instancing/batching strategy rather than creating needless per-object material copies.
- **Precision:** use `half` by default for color, masks, and alpha; use `float` where range or precision matters, such as world positions, time, and atlas UVs. Confirm support and precision needs on the target platform.
- **Shader targets:** the original preference is `#pragma target 3.0` for world shaders and `2.0` for UI shaders. Adapt these targets to the active pipeline, passes, required features, and supported devices; do not force an unsupported target or newer API.
- **UV work:** compute UV math in the vertex shader and pass it through interpolators. Use dependent texture reads or fragment-stage UV computation only where there is no suitable alternative.
- **Variants:** use `shader_feature_local` / `multi_compile_local` for new feature variants rather than global `multi_compile`. Keep variant counts controlled. An installed pipeline's required global keywords are a compatibility exception to document, not a reason to make feature keywords global.
- **Pass cost:** unless already explicitly requested or approved, do not enable previously disabled opaque/depth textures (URP: `_CameraOpaqueTexture` / `_CameraDepthTexture`), HDR, real-time shadows, or add full-screen renderer passes. Establish which extra copies, passes, bandwidth, and overdraw the change would add. Consider whether a static or infrequently changing result can be baked before adding a new `ScriptableRendererFeature` or equivalent pipeline pass. Follow the installed pipeline's Render Graph/API requirements.
- **Fragment operations:** do not introduce world-shader `clip()`/`discard`, variable-iteration fragment loops, or branching on non-uniform fragment values without an explicit requirement/approval and a justified target-specific cost assessment. UI masking such as `UNITY_UI_ALPHACLIP` is an allowed masking case. Alpha discard can impair early-Z on tile-based GPUs; do not treat all devices as identical.
- **Static backgrounds:** do not add per-pixel procedural full-screen evaluation for a static image; bake it to a texture. Keep genuinely dynamic requirements explicit and assess their cost.
- **GrabPass:** do not use it in URP, where it is unsupported. In a Built-in project, keep the same explicit approval and cost-review requirement for expensive framebuffer copies rather than treating URP APIs as an alternative.
- **Shader Graph is off by default.** Prefer hand-written HLSL for diff review and variant control. Use Shader Graph only when explicitly requested or when a verified existing Shader Graph workflow requires adapting this preference; do not convert existing graphs as incidental work.
- **Hardware constraints:** retain concrete platform budgets after verification, including fill-rate/overdraw constraints on tile-based devices where relevant. Do not assert that the source project's measured bottleneck applies to another game.
- **Verification:** compile changed shaders in the target Editor when available. Say exactly what was checked; compilation and functional success do not establish GPU cost. Use Frame Debugger and a device/GPU profiler where needed, and explicitly record unavailable checks rather than claiming the shader works.

### Unity assets and temporary verification

- Let Unity generate `.meta` files and GUIDs. When moving, renaming, or deleting an owned asset, handle its existing sibling `.meta` too; never invent GUIDs.
- Use Editor APIs/tools to create or modify serialized Unity assets and temporary test resources when the task requires them. Do not silently hand-edit scenes, prefabs, materials, or serialized settings. Restore only changes caused by the task's tests, preserving concurrent user edits.
- New code, necessary test helpers, and reports are within a requested feature workflow. Keep logs and XML results in temporary storage; record evidence paths without committing generated noise.
- Keep existing tests. Tests created solely for `feature-cycle` verification are temporary by default; retain them only when the user explicitly requests it. Follow the skill's cleanup and final verification steps.
