# AI Unity Pipeline

Project rules and reusable skills for Codex and Claude Code in existing Unity projects. Set up rules first, then custom skills, official Unity skills, and the Unity connection. For 3D asset authoring, optionally add the Blender workflow below. Instructions are in English; generated reports and chat summaries follow the user's language.

## 1. Installation

### Step 1: Copy the agent rules

Clone this repository into a tools folder outside the target Unity project:

```bash
git clone https://github.com/SinlessDevil/AI-UnityPipeline.git
```

For a private repository, authenticate with a GitHub account that has access. Perform installation on the computer where the agents will run.

Copy these files into the target project's root, alongside `Assets`, `Packages`, and `ProjectSettings`:

| Source | Destination | Agent |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | `<UnityProject>/AGENTS.md` | Codex |
| [CLAUDE.md](CLAUDE.md) | `<UnityProject>/CLAUDE.md` | Claude Code |

If either destination already exists, preserve it and use the update instructions below. These files came from a particular Unity project and must be adapted before use in another project.

### Step 2: Adapt the rules to the current project

Inspect the target project's version, packages, settings, code, and conventions. Update both files consistently. Change only project-specific mismatches; keep the remaining rules as they are.

| Area | What to adapt |
| --- | --- |
| Unity version | Read `ProjectSettings/ProjectVersion.txt` and use that exact version. Replace the source project's `6000.5.3f1` references. Do not upgrade Unity as part of setup. |
| Rendering | Identify the actual pipeline and package version. Keep URP rules only for URP. For Built-in, use Built-in shader and rendering conventions; for HDRP, use the project's HDRP conventions. Remove incompatible tags, includes, shader targets, and render-feature assumptions. |
| UI and editor tools | Follow the existing choice: uGUI, UI Toolkit, IMGUI editor tools, or inspector-only tooling. Replace blanket requirements that conflict with the project. |
| Architecture and dependency management | Keep Zenject instructions only if Zenject is used. Otherwise describe the actual composition and initialization approach, including existing singletons if applicable, or remove the Zenject section. Do not introduce a dependency framework to match this template. |
| Packages | Keep UniTask, DOTween, Addressables, billing, and other package-specific rules only where applicable. Document the project's existing alternatives. |
| Platforms and performance | Replace TV-only, Android, graphics API, and performance assumptions with the project's actual targets and constraints. |
| Paths and lifecycle | Correct namespaces, assemblies, folders, entry points, scenes, save systems, and resource paths. Remove references to source-project classes that do not exist. |
| Git and verification | Record actual branches, integration conventions, commit style, test locations, and build or test commands. |

Keep unaffected code style, change-scope, asset hygiene, and other working rules. Adapt the instructions to the project without refactoring the project to fit the instructions.

Example request:

```text
Adapt AGENTS.md and CLAUDE.md to this Unity project. Inspect its pinned
Editor version, render pipeline, UI and editor tooling, architecture,
packages, folders, Git workflow, and verification commands. Change only
project-specific mismatches and keep the remaining rules unchanged.
Keep both files consistent. Do not change game code or project settings.
```

### Step 3: Install custom skills

Install `feature-cycle` and `chat-notes` first, in this order. Add `blender-props` when you want to create or edit 3D props:

| Skill | Purpose | Example |
| --- | --- | --- |
| [feature-cycle](feature-cycle/SKILL.md) | Implement a Unity feature in a dedicated branch, verify it in Unity, fix failures, remove temporary tests, and commit the result with a Markdown status report. | `Use $feature-cycle to add saved puzzle progress.` |
| [chat-notes](chat-notes/SKILL.md) | Save conversation decisions, results, and remaining tasks in a dated Markdown file in the project's documentation folder. | `Use $chat-notes to save this conversation.` |
| [blender-props](blender-props/SKILL.md) — optional | Create editable Blender props from references, with materials, basic rigs, preview renders, and checked FBX exports for Unity. | `Use $blender-props to create a wooden table from these references.` |

For Codex, ask:

```text
Use $skill-installer to install feature-cycle, then chat-notes, from
https://github.com/SinlessDevil/AI-UnityPipeline.
These skill folders are at the repository root. Check existing user-level
and project-level installations first; install only missing skills.
```

For Blender modeling, also ask:

```text
Use $skill-installer to install blender-props from
https://github.com/SinlessDevil/AI-UnityPipeline.
The skill folder is at the repository root. Check existing user-level
and project-level installations first; install it only if missing.
```

For manual installation, copy each complete skill folder, including `SKILL.md`, `agents/openai.yaml`, and any supporting `references/` or `scripts/`, into one appropriate location:

| Agent | All projects for this user | This project only |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<UnityProject>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<UnityProject>/.claude/skills/` |

Existing Codex setups may also use `~/.codex/skills/`, including the bundled installer's default destination. Check that location before adding a duplicate. Keep one installation per skill for each agent. If a skill is not visible, start a new session.

Feature Cycle needs the pinned Unity Editor and a usable license for verification. Chat Notes does not require a Unity connection. Blender Props needs a local Blender executable with Python support and permission to write the requested asset files; its modeling and FBX checks do not require a Unity connection.

### Step 4: Install official Unity skills

After the custom skills, add Unity's official skills. For Codex and Claude Code on Unity 6+, Unity recommends the [official Unity plugin](https://github.com/Unity-Technologies/unity-agent-plugin), which distributes its skills together. Install it only for the agents you use; skip an existing enabled installation.

For Codex, run in a terminal:

```bash
codex plugin marketplace add Unity-Technologies/unity-agent-plugin
codex plugin add unity@unity-agent-plugin
codex plugin list
```

For Claude Code, enter these slash commands inside a Claude Code session:

```text
/plugin marketplace add Unity-Technologies/unity-agent-plugin
/plugin install unity@unity-agent-plugin
```

Check the installation with `/plugin`. For clients without plugin support, the [official Unity skills repository](https://github.com/Unity-Technologies/skills) provides an alternative requiring Node.js and npm:

```bash
npx skills add Unity-Technologies/skills
```

Choose the intended agent and scope in the installer. Use one distribution method per agent to avoid duplicate skills. Apply guidance only when compatible with the project's version, pipeline, and packages. Unity's current plugin targets Unity 6+. On older projects, skip the plugin and the connection below; use standalone guidance only after checking compatibility.

### Step 5: Install and connect Unity MCP for Unity 6+

Check `ProjectSettings/ProjectVersion.txt` first. The official Unity Pipeline connection requires Unity 6.0 or later. On older versions, skip this step and keep the existing workflow.

Unity's current MCP server runs through the Unity CLI. The older MCP server inside `com.unity.ai.assistant` is deprecated; for a legacy connection, follow the [official migration guidance](https://docs.unity.com/en-us/unity-cli/replace-mcp-server-unity-cli).

**Install the CLI if missing.** Check `unity --version`. If unavailable, follow the [Unity CLI installation guide](https://docs.unity.com/en-us/unity-cli/use-unity-cli). Choose the command for your operating system:

```bash
# macOS with Homebrew
brew install --cask unity-cli
```

```powershell
# Windows with winget
winget install Unity.CLI
```

For Linux or installation without these package managers, use the official guide above. Reopen the terminal and check `unity --version` again.

**Install the Editor bridge if missing.** Open the target project in its pinned Unity Editor. Following the [Unity Pipeline package guide](https://docs.unity.com/en-us/unity-cli/unity-pipeline/unity-pipeline-package), sign in and install the bridge for that project:

```bash
unity auth login
unity pipeline install --project-path "/absolute/path/to/UnityProject"
unity pipeline list
```

Wait for Unity to finish importing and compiling. The bridge installation changes the project's package setup; inspect the resulting package changes. If the bridge is already installed and healthy, skip installation.

**Register the MCP connection if missing.** Inspect existing client entries, including any supplied by the plugin. Keep a working connection to this project. Otherwise list supported clients:

```bash
unity mcp configure --list
```

Run only the command for the client you use:

```bash
# Codex
unity mcp configure codex --project-path "/absolute/path/to/UnityProject"

# Claude Code
unity mcp configure claude-code --project-path "/absolute/path/to/UnityProject"
```

See Unity's [MCP configuration reference](https://github.com/Unity-Technologies/unity-agent-plugin/blob/main/skills/unity-cli/references/integration-advanced.md) for client support and project targeting. If your installed CLI does not list the desired client, add a stdio server through that client's MCP settings: executable = the absolute path to `unity`; arguments = `mcp`, `--project-path`, and the absolute project path. Preserve other MCP entries.

Restart or reconnect the agent. Confirm that Unity tools are available and make a read-only request to identify the project and read Editor status or Console output. Verify the connected project path. Record failures accurately. Shell-capable agents can also use direct Unity CLI commands; register MCP when using the MCP interface.

### Step 6: Optional Blender asset workflow

Install [blender-props](blender-props/SKILL.md) from Step 3 when 3D prop authoring is wanted. Use an existing Blender installation and verify its executable with `--version`; an executable absent from PATH may still be installed through Steam or in a custom folder. Ask for the executable path if it cannot be located. Do not upgrade or install Blender merely because an optional component is absent.

The workflow uses Blender's built-in Python API (`bpy`) through the executable. A separate Blender MCP server, Blender add-on, or paid asset-generation service is not required. The initial table/book/lamp test used this API directly; this skill captures that process for reuse. It is a custom skill in this repository, not part of Unity's official plugin.

A Windows example, replacing the path with the local installation:

```powershell
$blenderExe = 'E:\Utilities\Steam\steamapps\common\Blender\blender.exe'
& $blenderExe --version
& $blenderExe --background --python-exit-code 1 --python 'ArtSource/MyProps/build_props.py'
if ($LASTEXITCODE -ne 0) { throw 'Blender asset build failed' }
```

The build script is created for the requested asset; `build_props.py` is an example filename, not a bundled generator. The process was exercised with Blender **5.2.3 LTS** on Windows. Use the installed version's API and verify exports when adapting it to another version.

Provide references, the intended scale/style, required motion, and the Blender path when known. An asset request authorizes the relevant model, texture, preview, and build-script outputs within the agreed location; it does not call for changing unrelated Unity assets, game logic, project settings, or the existing code-only defaults.

Example request:

```text
Use $blender-props to create a stylized wooden table, an open book with
blank white pages and a closing rig, and a desk lamp from these references.
Use this Blender executable: <absolute path to blender.exe>.
Save editable sources, textures, separate FBX exports, and preview renders
in ArtSource/DeskProps. Check the open, intermediate, and closed poses.
Report Blender/FBX verification separately from Unity verification.
```

Expected deliverables:

- An editable `.blend` with resolved/packed textures, plus a reproducible build script where procedural construction is appropriate.
- Separate FBX files with intentional metre scale, pivots, and only the required geometry/rig.
- Baked image textures for important procedural materials; Blender node graphs are not automatically Unity materials.
- Inspected previews and, for animated props, documented clips, controls, and checks of bones plus shape-key deformation after FBX reimport.
- A short usage note with any remaining Unity import/material setup.

Keep authoring sources outside `Assets` for explicit FBX delivery. Import into Unity and create materials/prefabs through the Editor when that integration is requested. Preserve Unity-generated GUIDs and the project's rendering conventions. A correct Blender render or Blender → FBX → Blender check does **not** establish that URP materials or animation work in Unity; verify that separately or mark it pending.

## 2. Update Instructions

Treat a general request to update this setup as a check-and-complete operation: inspect existing components, preserve what works, and install only what is missing. Updating an installed component to a newer version requires an explicit version-update request.

### Step 1: Inspect what exists

Check both rule files, all relevant skill scopes, installed Unity plugins, the Unity version, CLI, Pipeline package, and MCP entries. Plugins may already supply the skills or connection. Check actual availability, not just whether a folder exists. For projects using Blender authoring, also check `blender-props` and the configured Blender executable/version; otherwise mark those optional components as not applicable.

| Component | If present and working | If missing |
| --- | --- | --- |
| `AGENTS.md` / `CLAUDE.md` | Keep the adapted project rules; do not download replacements over them. | Copy only the missing file and adapt it to this project and the other rule file. |
| `feature-cycle` / `chat-notes` | Keep the installed skill; do not reinstall in another scope. | Install only the missing skill from this repository. |
| `blender-props` (optional) | Keep the installed skill and local adaptations. | Install from this repository when Blender prop authoring is wanted. |
| Blender executable (optional) | Keep the working executable/version and local path. | Locate an existing installation; if absent, report the prerequisite and obtain authorization before installing it. |
| Official Unity skills or plugin | Keep the existing compatible distribution. | Install a compatible official distribution for the intended agent. |
| Unity CLI | Keep the working installation. | Install if the chosen Unity 6+ connection needs it. |
| Unity Pipeline package | Keep the healthy compatible package. | Install when setting up the Unity 6+ connection. |
| Unity MCP connection | Keep a working connection to the correct project. | Configure the client after checking for a plugin-provided connection. |

If something exists but is broken or incomplete, repair the specific issue without overwriting customizations or creating duplicates. On Unity versions older than 6, mark the official connection as not applicable; do not upgrade the Editor.

### Step 2: Obtain only missing components

Use the corresponding installation step above for each missing component. If nothing is missing, report that setup is complete without reinstalling it.

If a local source checkout is needed, check that it has no uncommitted edits before refreshing it:

```bash
git -C "/path/to/AI-UnityPipeline" pull --ff-only
```

Pulling this repository does not update files or skills previously copied into a project or user directory.

### Step 3: Preserve adaptations and verify

Keep project-specific rendering, UI, dependency management, version, platform, and workflow decisions. If the user explicitly requests newer rule contents, compare upstream changes and merge relevant changes into the adapted files rather than replacing them wholesale.

For an explicit skill or plugin version update, use the original installation method and preserve local edits. The Codex skill installer refuses to overwrite an existing skill folder; it is not an in-place updater. Do not delete an installation just to bypass that check. Compare and merge changes deliberately. Update the CLI through the package manager or installation method that owns it, and check compatibility before changing Editor packages.

Confirm that both rule files match the project, skills are discoverable without duplicates, and the Unity connection works where applicable. Report what was already present, added, repaired, or skipped, and any remaining blocker. Claim connection verification only after a request reaches the intended Editor. For the Blender workflow, distinguish executable detection, inspected source/render output, FBX round-trip checks, and actual Unity import/playback verification. Do not rebuild an existing asset set merely to update the skill.

Example update request:

```text
Check and complete this project's AI Unity Pipeline setup using
https://github.com/SinlessDevil/AI-UnityPipeline.
Inspect existing rules, skills, plugins, Unity version, CLI, Pipeline
package, and MCP connections first. If Blender prop authoring is enabled,
also check blender-props and the Blender executable. Preserve working installations and
project customizations. Install only missing components, repair specific
failures, and do not create duplicates. Skip the official Editor connection
on Unity versions older than 6. Report changes and actual verification.
```
