# AGENTS.md

Shared working rules for Codex and Claude Code. Read [README.md](README.md) for installation and update instructions.

## Scope and adaptation

AI-UnityPipeline is a toolkit of instructions and skills, not a Unity game. It has no Editor version, render pipeline, scenes, gameplay assemblies, or Unity build to run. When maintaining this repository, edit only the requested instructions, metadata, and supporting resources; validate Markdown links, skill frontmatter, YAML, and the final diff. Do not modify Unity projects elsewhere on the machine.

When copying these rules into a Unity project, adapt the target-project guidance below to that project's verified facts. Keep the scope distinction until adaptation is complete: do not treat missing Unity files in this toolkit as broken project wiring. Keep both agent entry points available; `CLAUDE.md` delegates shared rules to this file.

User instructions and environment permissions take precedence. Task-specific workflow requests can override defaults here, but do not override an explicit current restriction or grant unavailable access.

## Branches and commits

- Check Git status and actual local/remote branches before changing branches. Preserve unrelated or unfinished work; use a separate worktree when needed.
- Develop each feature in `feature/<short-name>` from the user-specified base or actual integration branch. Use `dev` where established; this toolkit currently uses `main`. Do not invent `dev` or a release branch.
- Keep the feature branch for review. When integration is requested, use a squash merge unless the target project specifies otherwise. Push, pull request creation, and merge require task authorization.
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

### Architecture and code

- Preserve the existing composition root, dependency direction, state/scene transitions, initialization, and resource ownership. Do not impose a new architecture, singleton policy, or UI pattern as part of a feature.
- If Zenject is present, register new services in the actual installer and respect binding scope, initialization, ticking, and disposal. Otherwise follow the project's existing dependency management. Use UniTask, Addressables, DOTween, or other integrations only where already adopted or explicitly requested.
- Follow established C# style. Default conventions when none are specified: Allman braces, `_camelCase` private fields, `readonly` where appropriate, `var` for obvious local types, and expression-bodied one-liners. Keep helpers in the project's established extension/helper folders.
- Do not silently swallow missing required bindings or serialized references. Validate wiring clearly at appropriate boundaries. Handle expected optional values, destroyed Unity objects, cancellation, and teardown states explicitly where the lifecycle requires it.
- Use existing resource-path constants, factories, initialization idioms, and save abstractions. Do not assume a class such as `BootstrapInstaller` or `ResourcePath` exists.

### UI and rendering

- Follow the project's actual runtime UI and editor tooling: uGUI, UI Toolkit, IMGUI, or inspector-only tools as applicable. Keep presentation separate from business logic where the project does so; do not migrate existing screens to a new pattern without a requirement.
- Determine the active render pipeline, renderer configuration, installed package versions, build targets, and graphics APIs. Do not equate Unity 6 with URP 14 or assume a fixed Forward renderer. Use documentation matching the resolved packages.
- For URP shaders, follow the installed URP's HLSL includes, pipeline tags, and SRP Batcher layout where applicable. For Built-in or HDRP, follow that pipeline's conventions instead. Shader targets, precision, keyword scope, Render Graph integration, and Shader Graph use depend on project requirements.
- Evaluate material instances and MaterialPropertyBlocks against the actual batching/instancing strategy and resource ownership. Do not replace them categorically with per-object materials.
- New depth/opaque textures, fullscreen passes, shadows, HDR, transparency, fragment branching, or procedural effects require a justified cost assessment for the target. Do not ban valid rendering techniques or claim a bottleneck without evidence; keep settings changes within the authorized feature.
- Compile changed shaders in the target Editor when available. Functional or compilation success does not establish GPU cost: use Frame Debugger and an appropriate profiler/device check when needed, and report unavailable checks.

### Unity assets and temporary verification

- Let Unity generate `.meta` files and GUIDs. When moving, renaming, or deleting an owned asset, handle its existing sibling `.meta` too; never invent GUIDs.
- Use Editor APIs/tools to create or modify serialized Unity assets and temporary test resources when the task requires them. Do not silently hand-edit scenes, prefabs, materials, or serialized settings. Restore only changes caused by the task's tests, preserving concurrent user edits.
- New code, necessary test helpers, and reports are within a requested feature workflow. Keep logs and XML results in temporary storage; record evidence paths without committing generated noise.
- Keep existing tests. Tests created solely for `feature-cycle` verification are temporary by default; retain them only when the user explicitly requests it. Follow the skill's cleanup and final verification steps.
