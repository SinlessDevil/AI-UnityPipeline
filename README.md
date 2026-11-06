# AI Unity Pipeline

Reusable Codex skills for Unity development and preserving conversation context. All skill instructions and interface metadata are written in English. Generated reports and chat summaries follow the user's language.

## Skills

| Skill | Purpose |
| --- | --- |
| [feature-cycle](feature-cycle/SKILL.md) | Implement a Unity feature in a dedicated branch, verify it in Unity, fix failures, remove temporary tests, and commit the result with a Markdown status report. |
| [chat-notes](chat-notes/SKILL.md) | Save the current conversation's decisions, results, and remaining work in a dated Markdown file under the project's documentation folder. |

## Installation

On another computer, ask Codex:

```text
Use $skill-installer to install feature-cycle and chat-notes from
https://github.com/SinlessDevil/AI-UnityPipeline.
The skill folders are feature-cycle and chat-notes at the repository root.
```

For a private repository, authenticate with a GitHub account that has access. The installer needs to run on the computer where you want the skills installed. If newly installed skills do not appear, restart Codex.

Alternatively, clone the repository and copy the complete `feature-cycle` and `chat-notes` folders into a supported local skills directory, such as `~/.agents/skills/`, or into `.agents/skills/` inside a project for project-specific use. Existing Codex setups using `~/.codex/skills/` can use that location with the bundled installer.

The installer refuses to overwrite an existing skill folder. To update an existing installation, replace its contents with the latest version from this repository while preserving any local customizations you need.

## Usage

In a Unity project, describe the desired feature:

```text
Use $feature-cycle to add saved progress for puzzle placement.
```

The workflow runs the project's pinned Unity Editor and requires an available Editor installation and license. It follows project architecture and conventions, preserves unrelated work, and records actual verification results. It leaves the feature branch for review; pushing, opening a pull request, and merging require a separate request.

To preserve a conversation:

```text
Use $chat-notes to save the decisions and results from this chat.
```

This creates a summary such as `Docs/YYYY-MM-DD-short-topic.md` without changing code or committing it.
