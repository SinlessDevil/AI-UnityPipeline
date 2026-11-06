# AI Unity Pipeline

Project rules and reusable skills for Codex and Claude Code in existing Unity projects. This repository is a toolkit, not a Unity project: do not run Unity builds here or modify external projects while maintaining it. Set up rules first, then custom skills, official Unity skills, and the Unity connection. Instructions are in English; generated reports and chat summaries follow the user's language.

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

If either destination already exists, preserve it and use the update instructions below. Copy both files: `AGENTS.md` holds shared rules and target-project guidance; `CLAUDE.md` tells Claude Code to read that same file. Adapt the guidance before applying it to a Unity project. These templates do not assume an installed game architecture.

### Step 2: Adapt the rules to the current project

Inspect the target project's version, packages, settings, code, and conventions. Adapt the target-project guidance in `AGENTS.md`, preserving the shared reference from `CLAUDE.md` and any existing Claude-specific rules. After adaptation, distinguish rules for maintaining this toolkit from rules for working in the target Unity project; the toolkit-only restriction on external projects must not prohibit work in the chosen target. Change only project-specific mismatches; keep the remaining rules as they are.

| Area | What to adapt |
| --- | --- |
| Unity version | Read `ProjectSettings/ProjectVersion.txt` and use that exact version. Resolve package versions from the manifest/lockfile; do not pair an Editor with an assumed URP version. Do not upgrade Unity as part of setup. |
| Rendering | Identify the actual pipeline and package version. Keep URP rules only for URP. For Built-in, use Built-in shader and rendering conventions; for HDRP, use the project's HDRP conventions. Remove incompatible tags, includes, shader targets, and render-feature assumptions. |
| UI and editor tools | Follow the existing choice: uGUI, UI Toolkit, IMGUI editor tools, or inspector-only tooling. Replace blanket requirements that conflict with the project. |
| Architecture and dependency management | Keep Zenject instructions only if Zenject is used. Otherwise describe the actual composition and initialization approach, including existing singletons if applicable, or remove the Zenject section. Do not introduce a dependency framework to match this template. |
| Packages | Keep UniTask, DOTween, Addressables, billing, and other package-specific rules only where applicable. Document the project's existing alternatives. |
| Platforms and performance | Record actual target platforms, graphics APIs, and performance constraints. Do not assume TV-only behavior or a measured bottleneck. |
| Paths and lifecycle | Record actual namespaces, assemblies, folders, entry points, scenes, save systems, resource paths, and lifetime/ownership conventions. |
| Git and verification | Record actual branches, integration conventions, commit style, test locations, and available verification tools. `feature-cycle` includes temporary tests, Editor-created test resources, review, and reports; optional-testing defaults must not prohibit that requested workflow. |

Keep unaffected code style, change-scope, asset hygiene, and other working rules. Adapt the instructions to the project without refactoring the project to fit the instructions.

Example request:

```text
Adapt AGENTS.md and CLAUDE.md to this Unity project. Inspect its pinned
Editor version, render pipeline, UI and editor tooling, architecture,
packages, folders, Git workflow, and verification commands. Change only
project-specific mismatches and keep the remaining rules unchanged.
Keep both files consistent. Do not change game code or project settings.
```

### Step 3: Install the two custom skills

Install these first, in this order:

| Skill | Purpose | Example |
| --- | --- | --- |
| [feature-cycle](feature-cycle/SKILL.md) | Implement a Unity feature in a dedicated branch, run functional checks and mandatory Performance & Reliability Code Review, fix confirmed issues, remove temporary tests, verify the final tree, and commit with a Markdown status report. | `Use $feature-cycle to add saved puzzle progress.` |
| [chat-notes](chat-notes/SKILL.md) | Save conversation decisions, results, and remaining tasks in a dated Markdown file in the project's documentation folder. | `Use $chat-notes to save this conversation.` |

For Codex, ask:

```text
Use $skill-installer to install feature-cycle, then chat-notes, from
https://github.com/SinlessDevil/AI-UnityPipeline.
Both skill folders are at the repository root. Check existing user-level
and project-level installations first; install only missing skills.
```

For manual installation, copy each complete skill folder, including `SKILL.md` and `agents/openai.yaml`, into one appropriate location:

| Agent | All projects for this user | This project only |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<UnityProject>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<UnityProject>/.claude/skills/` |

Existing Codex setups may also use `~/.codex/skills/`, including the bundled installer's default destination. Check that location before adding a duplicate. Keep one installation per skill for each agent. If a skill is not visible, start a new session.

`feature-cycle` follows this order: implementation → functional verification → Performance & Reliability Code Review and scoped fixes/rechecks → temporary test cleanup → final-tree verification → status report and feature-branch commit. Review covers the complete feature diff and only relevant GC/memory, CPU, lifecycle/reliability, and UI/rendering paths. Its [review reference](feature-cycle/references/performance-reliability-review.md) defines P0/P1/P2, evidence requirements, independent review or an explicit second pass, and a no-progress stopping rule. No separate review skill is needed.

The single `Status.md` records functional results, review results and fixed findings, unresolved confirmed findings and unconfirmed risks, rechecks, cleanup/final verification, limits, and required Profiler/device actions. Missing Editor execution is reported as incomplete; missing profiling limits performance claims and blocks readiness only when the acceptance criteria require that measurement. Existing tests are preserved; temporary checks are kept only on explicit request or while needed to diagnose a blocked run. Feature Cycle needs the pinned Unity Editor and a usable license for functional verification. Chat Notes retains its summary-only scope and does not require a Unity connection.

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

## 2. Update Instructions

Treat a general request to update this setup as a check-and-complete operation: inspect existing components, preserve what works, and install only what is missing. Updating an installed component to a newer version requires an explicit version-update request.

### Step 1: Inspect what exists

Check both rule files, all relevant skill scopes, installed Unity plugins, the Unity version, CLI, Pipeline package, and MCP entries. Plugins may already supply the skills or connection. Check actual availability, not just whether a folder exists.

| Component | If present and working | If missing |
| --- | --- | --- |
| `AGENTS.md` / `CLAUDE.md` | Keep the adapted project rules; merge relevant upstream changes only when requested. | Copy the missing file, preserve existing rules, and ensure Claude's shared reference resolves before adapting it. |
| `feature-cycle` / `chat-notes` | Keep the installed skill; do not reinstall in another scope. | Install only the missing skill from this repository. |
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

Confirm that both rule entry points resolve consistently for the project, skills are discoverable without duplicates, and the Unity connection works where applicable. When updating `feature-cycle`, include its `references/` folder and metadata so the review procedure is installed too. Report what was already present, added, repaired, or skipped, and any remaining blocker. Claim connection verification only after a request reaches the intended Editor.

Example update request:

```text
Check and complete this project's AI Unity Pipeline setup using
https://github.com/SinlessDevil/AI-UnityPipeline.
Inspect existing rules, skills, plugins, Unity version, CLI, Pipeline
package, and MCP connections first. Preserve working installations and
project customizations. Install only missing components, repair specific
failures, and do not create duplicates. Skip the official Editor connection
on Unity versions older than 6. Report changes and actual verification.
```
