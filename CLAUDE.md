# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A production Unity game template for mobile + Android TV, built on **Zenject** DI and **Unity Addressables**. The `README.md` is detailed and authoritative on architecture — read it before large changes. Note: `README.md` claims Unity 2023.2.22f1, but the actual editor is pinned in `ProjectSettings/ProjectVersion.txt` (**6000.5.3f1**) — trust the latter.

## Commands

There is no CLI build/test wrapper in this repo. Everything runs through the Unity Editor or `Unity.exe -batchmode`.

- **Run the game:** open `Assets/Scenes/Initial.unity` (the only scene in Build Settings) and enter Play Mode. All other scenes load via Addressables.
- **First-time setup / after touching addressable assets:** *Window → Asset Management → Addressables → Groups* → *Build → New Build → Default Build Script*. To iterate without rebuilding bundles, set **Play Mode Script** to *Use Asset Database*.
- **Tests:** *Window → General → Test Runner* (EditMode + PlayMode tabs), or the project's own *Tools → Tests Tool Window*. Tests live in `Assets/Tests/{EditMode,PlayMode}` under the `Tests.EditMode` / `Tests.PlayMode` asmdefs.
- **Batch-mode tests (CI):** `Unity.exe -runTests -batchmode -projectPath . -testPlatform EditMode -testResults results.xml` (swap `PlayMode` for the other suite). To run one test, add `-testFilter "Namespace.ClassName.TestName"`.

### Editor dev tools (custom menu items)

- *GameEditors → ⚙ Game Config Editor* (`%F3` / Ctrl+F3) — central config editor
- *Tools → IAP Validation Window* — validates the `SubscriptionsConfig` subscriptions and their child/parent SKUs
- *Tools → TV Validation Window* — TV focus/navigation validation
- *Tools → Audio Window/Sound Library*, *Tools → Save Window/...*, *Tools → Text Migration Window*

## Compile symbols (purchasing)

Purchasing code is gated behind scripting-define symbols — large parts of `BootstrapInstaller`, `BootstrapAnalyticState`, and the whole `Services/Purchases` tree are `#if`-wrapped. When editing those files, know which symbols are active or code will appear dead:

- `WBILLING` — UniWrapper Billing backend + all billing-dependent bindings
- `UNI_WRAPPER` — the whole `Uni.Wrapper` package (ads, analytics, rate-us, premium-state sync)
- `WPURCHASING` — retired. The Unity IAP backend and its `IAPBillingAdapter` bridge were deleted; only `Services/Purchases/IAPProduct` is kept, `#if WPURCHASING`-fenced and never compiled, as a reference for the old catalog-based flow.

Game code never touches the `#if`-gated purchasing tree directly: it goes through `IPremiumService` (perk/availability queries, purchases) and `IOfferService` (the offer popup), both of which always compile. Neither may take `IBillingProductService`/`ISubscriptionProductService` as a constructor dependency — see the note in `PremiumService`.

## Architecture (big picture)

Strict dependency direction: **Infrastructure → Services → Game Logic**. Code namespace root is `Code`; all gameplay/runtime code is in the `Game` asmdef (`Assets/Code/Game.asmdef`), editor code in `GameEditor`.

**Composition root — `BootstrapInstaller` (`Assets/Code/Infrastructure/Installers/`).** A Zenject `MonoInstaller` on the `GameRunner` prefab. `InstallBindings()` wires every service (`Bind*` methods), then `Initialize()` → `BootstrapGame()` enters the state machine at `BootstrapState`. To add a service: register it in the appropriate `Bind*` method here. Three static-data services (`StaticDataService`, `AudioVibrationStaticDataService`, `TVStaticDataService`) are constructed and `.LoadData()`/`.LoadConfig()`-called eagerly in `BindStaticDataService()` before binding — they must be available synchronously.

**Game flow — `IStateMachine<IGameState>`.** Linear state chain, each state injected via Zenject (no service locator):
`BootstrapState → LoadProgressState → BootstrapAnalyticState → PreLoadGameState → LoadMenuState → LoadLevelState → GameLoopState` (→ Win/Lose). States are bound in `BindGameStates()` and live in `Infrastructure/StateMachine/Game/States/`. `BootstrapAnalyticState` is where purchasing initializes (`PurchasingBootstrapInstaller.InitializeAsync()`, `#if WBILLING`).

**TV platform layer.** The project ships **TV-only**: `BootstrapState.Enter()` hardcodes `isTv = true`, and `PlatformDetect` / `GameConfig.DebugPlatform` were deleted along with the phone path. `StaticDataService.SetPlatformMode(isTv)` records the `IsTv` flag and `UIFactory` then picks TV vs base asset paths. Window configs are **not** platform-switched any more: the project ships TV-only, so `TVWindowsStaticData` is the single window config (the base `WindowsStaticData` and the merge-over-base logic were dropped). TV MonoBehaviours (`TVScreen`, `TVSelectable`) reach services through the static `TVPlatformBootstrap` locator since they can't be Zenject-injected. Removing TV support = drop the `BindTVServices()` call + TV params in `BootstrapState`.

**Asset management — `AssetProvider`.** Addressables cache with two stores: a **temp** cache cleared on scene change (`CleanUp()`) and a **persistence** cache that's never cleared. `SceneLoader` releases the previous scene handle before each load. Windows (`WindowConfig` → `AssetReferenceGameObject`) load through the temp cache and free automatically on scene transition.

**Static data.** ScriptableObjects under `Assets/Resources/StaticData/`, loaded synchronously at boot. See the README table for the full asset → path map (`GameConfig`, `Balance`, `WindowsStaticData` / `TVWindowsStaticData`, `Sounds`, `TVConfig`, `SubscriptionsConfig`, etc.).

**Save system.** `ISaveLoadFacade` (`UnifiedSaveLoadFacade`) dispatches per-call between PlayerPrefs (`PrefsSaveLoadService`) and JSON (`JsonSaveLoadService`) via a `SaveMethod` enum. Progress is read through `IPersistenceProgressService`.

## Development rules

These are the project's standing conventions — follow them for new code unless the user says otherwise.

### Stack
- Third-party plugins in use: **Zenject** (DI), **UniTask** (async), **DOTween** (tweens), **Addressables** (asset/scene loading), **UI Toolkit** (editor windows only — see UI rules). These are current and trusted; do not audit or second-guess them.
- Unity **6000.5.3f1** (`ProjectSettings/ProjectVersion.txt`) — write code against this version and the existing architecture, not newer APIs.

### Code style
- **Strict Microsoft C# style.** Private fields are `_camelCase` with a leading underscore; `readonly` wherever possible. Braces on their own lines (Allman). Use explicit types for C# local variables, loop variables and `out` declarations. Do not use `var`. Use expression-bodied members (`=>`) for one-liners (see `LevelService`).
- **Member order inside a type, top to bottom:** constants/`static readonly` → serialized/private fields → properties → events/Actions → constructor (plain or Zenject `Constructor()` init) → public methods → private methods. Keep new code in this order; mirror a neighbouring service.
- **No defensive null-checks.** Do not guard serialized/injected references (`if (_field != null) …`, `x == null → return`) just in case. A missing `.asset`, an unassigned inspector field or a forgotten binding must throw a loud `NullReferenceException` — that's how the user finds the wiring mistake. Write a null-check only when `null` is a real, expected state that the logic must branch on (e.g. "no pooled instance yet → create one", "unbound slot → fall back to the global input adapter").
- **Extensions go in `Assets/Code/Extensions`.** Reusable helper/extension methods belong there as `*Extensions` classes (e.g. `TransformExtensions`, `NumericExtensions`), not scattered inline. Add your own there when it makes sense.

### Shaders
- **The pipeline is URP 14 Forward, never Built-in.** Project shaders live in `Assets/Code/Shaders`, named `Custom/URP/<Name>`. Required: the `"RenderPipeline" = "UniversalPipeline"` tag, an `HLSLPROGRAM` block (not `CGPROGRAM`), and includes from `Packages/com.unity.render-pipelines.universal/ShaderLibrary/`. `UnityCG.cginc`, `UnityObjectToClipPos`, `fixed4` and surface shaders are Built-in — they must not appear in new code.
- **Target hardware:** Android Vulkan + GLES3 (no GLES2), plus Android TV. Tile-based GPUs, and the measured ceiling is fill rate / overdraw, not ALU.
- **Every shader must:**
  - Wrap all material properties in `CBUFFER_START(UnityPerMaterial) … CBUFFER_END`, or the renderer drops out of the SRP Batcher. For the same reason, don't drive per-instance values through a `MaterialPropertyBlock` — make a separate material.
  - Use `half` by default for colour/mask/alpha, `float` only where range matters (world position, time, atlas UV). The existing shaders already do this — mirror `WaterTiles` / `MenuBackground`.
  - Declare `#pragma target 3.0` for world shaders, `2.0` for UI shaders.
  - Compute UV math in the vertex shader and pass it through an interpolator; use dependent texture reads (UV computed in the fragment) only when there is no alternative.
  - Gate variants with `shader_feature_local` / `multi_compile_local` only — never a global `multi_compile`.
- **Not allowed without asking first:**
  - `_CameraOpaqueTexture` and `_CameraDepthTexture` — both are off in `Assets/Resources/URP/URP Asset.asset` (`m_RequireOpaqueTexture: 0`, `m_RequireDepthTexture: 0`). Requesting either turns on an extra full-screen pass for the whole game.
  - `GrabPass` (Built-in only, does nothing in URP), HDR effects (`m_SupportsHDR: 0`), real-time shadows (`m_MainLightShadowsSupported: 0`).
  - A new `ScriptableRendererFeature` with full-screen passes. Precedent: `ShadowMaskFeature` cost two full-screen passes every frame for a picture that changes once every few seconds, and was replaced by a CPU bake (`Code/Services/Shadows`). Before writing a pass, ask whether the result can be baked instead.
  - `clip()` / `discard` — it breaks early-Z on tile-based GPUs. Fine for UI masking (`UNITY_UI_ALPHACLIP`), not for world sprites.
  - Loops with a variable iteration count, and branching on non-uniform values in the fragment stage.
  - Per-pixel procedural full-screen backgrounds. If the image is static, bake it to a texture (see `MenuBackground`) instead of evaluating it every frame.
- **Shader Graph is off by default.** Write HLSL by hand — a graph can't be reviewed in a diff and explodes the variant count. Use it only when explicitly asked.
- **No local verification.** Shaders don't compile from here. After editing one, tell the user to recompile in Unity and check the Frame Debugger / on-device GPU profiler — never claim it "works".

### Folders (where things live)
- `Assets/Code` — all runtime/editor code.
- `Assets/Tests` — EditMode + PlayMode tests.
- `Assets/Resources/StaticData` — ScriptableObject configs (loaded synchronously at boot).
- `Assets/ResourcesAddresable` — prefabs/scenes spawned & loaded into memory via Addressables.

### Core patterns
- **Entry point = `BootstrapInstaller`** (`Assets/Code/Infrastructure/Installers/`). This is where everything is composed: services, factories, static-data, and the game state machine are all bound here. New service/factory ⇒ register it in the matching `Bind*` method.
- **State machine flow.** The app is driven by a strict state-machine chain (`IStateMachine<IGameState>`): switching screens, leaving menu, entering gameplay, win/lose all go through states in `Infrastructure/StateMachine/Game/States/`. Don't bypass it for navigation/flow.
- **Service-per-feature.** Each feature gets its own interface-first service(s): `IFooService` + `FooService`, injected via Zenject, bound with `Container.BindInterfacesTo<FooService>().AsSingle()`. Per-frame work uses `ITickable`; init that must run at bind time uses eager `Container.Resolve<...>()` in the installer (see `BindAudioService`). Mirror an existing service in `Assets/Code/Services` for structure.
- **Factories.** A complex entity (e.g. the player) gets its own dedicated Zenject factory deriving from `Factory` (`Services/Factories/Factory.cs`) — it loads the prefab via Addressables/`IAssetProvider`, instantiates through `IInstantiator`, and applies the entity's base setup. Async, returns `UniTask`. Trivial entities (a widget, a simple UI element) don't need a dedicated factory — go through a general factory like `UIFactory`. When unsure whether something is "complex enough", ask.
- **OOP / SOLID** are followed strictly — no service locators, no static singletons for runtime logic (the `TVPlatformBootstrap` static locator exists only because TV MonoBehaviours can't be Zenject-injected).
- **Async = UniTask**, not raw `Task` or coroutines, for new code.

### UI (when asked to build UI)
- Stack: **uGUI** (current windows use `RectTransform` + DOTween). Reserve **UI Toolkit** for editor tooling unless told otherwise.
- New UI follows **MVVM** (here VM = a presenter / presentation model):
  - **View** — only displays what's on screen (and may host its own animation), no business logic.
  - **ViewModel (presenter)** — the "conductor": pulls data from the model, computes/calculates presentation-ready values, and feeds the View.
  - **Model** — owns and serves the raw data.
- Scope: apply MVVM to **new UI only**. Leave existing `BaseWindow` / `StateWindow` / `IWindowState` windows (`Assets/Code/UI/Menu/Windows`) as-is — don't migrate them unless explicitly asked.

### Testing
- Unit tests are **optional and per-task**. After finishing a feature, **ask** whether unit tests are wanted in this context rather than writing them by default. Tests live in `Assets/Tests/{EditMode,PlayMode}`.

### TV / assets note
- Two parallel asset trees mirror base vs TV: `ResourcesAddresable/{Hud,UI}` ↔ `{TVHud,TVUI}`. Adding a screen usually means adding both variants and a `TVWindowsStaticData` override only if TV differs.

### Working in this repo via the filesystem (agent constraints)
- **Edit only code files by default** — `.cs`, plus `.shader`/`.hlsl` under `Assets/Code/Shaders`. You may *read* anything (`.meta`, `.asset`, `.prefab`, `.unity`, `.mat`, `.shadergraph`, `.uxml`/`.uss`, `.json`, configs) to understand the project, but only **edit/create those code files** unless the user explicitly asks you to change another file type. Never silently hand-edit Unity-serialized assets (`.prefab`, `.unity`, `.asset`, `.meta`) — those are owned by the Editor.
- **`.meta` / GUID hygiene.** This is a Unity project edited outside the Editor. Every asset/script has a sibling `.meta` with a unique GUID. Do **not** hand-author `.meta` files or invent GUIDs — Unity generates them on reimport, and `GuidDuplicationTest` fails on duplicates. When renaming/moving/deleting a file, move/delete its `.meta` alongside it. A newly created `.cs` will have no `.meta` until the user lets Unity recompile.
- **No local compile/test feedback loop.** Code is not compiled and Play Mode is not run from here — that happens in the Unity Editor. So: write carefully (no compiler safety net), and after non-trivial changes explicitly tell the user to recompile in Unity and/or run the Test Runner. Don't claim a change "works" — say it's written and needs an in-Editor build/test.
- **Addresses via `ResourcePath`.** Use the constants in `Code.Services.Factories.ResourcePath` for Addressables/Resources paths instead of inline magic strings. If a needed path isn't there yet, add a constant rather than hardcoding (some legacy paths are still inline — don't multiply them).
- **`Constructor()` init idiom.** Plain C# classes that aren't Zenject constructor-injected use a `public void Constructor(...)` init method (called manually after creation, ~13 places, e.g. `IWindowState.Constructor`). This is the project's init convention, not an actual C# constructor — follow it for similar classes and don't "fix" it into a real ctor.
